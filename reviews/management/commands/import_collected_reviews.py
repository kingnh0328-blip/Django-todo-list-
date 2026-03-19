import csv  # .csv 파일을 읽고 파싱할 수 있게 파이썬 내장 csv 기능을 불러와줘
import json  # .json 파일을 읽고 파싱할 수 있게 파이썬 내장 json 기능을 불러와줘
import hashlib  # 텍스트를 고유한 해시값으로 변환할 수 있게 파이썬 내장 hashlib 기능을 불러와줘 (중복 데이터 체크용)
from pathlib import (
    Path,
)  # 파일 경로를 다룰 수 있게 파이썬 내장 pathlib에서 Path 기능을 불러와줘
from datetime import (
    datetime,
)  # 날짜와 시간 값을 활용할 수 있게 파이썬 내장 datetime 모듈에서 datetime 클래스를 불러와줘

from django.core.management.base import (
    BaseCommand,
    CommandError,
)  # Django 커스텀 명령어를 만들 수 있게 django.core.management.base에서 BaseCommand(명령어 기본 틀)와 CommandError(오류 처리)를 불러와줘
from django.utils.dateparse import (
    parse_datetime,
)  # 문자열로 된 날짜/시간 데이터를 Django가 인식하는 datetime 형식으로 변환할 수 있게 django.utils.dateparse에서 parse_datetime을 불러와줘

from reviews.models import (
    CollectedReview,
)  # DB에 데이터를 저장할 수 있게 reviews/models.py에서 CollectedReview 모델 클래스를 불러와줘


def pick(
    d: dict, candidates: list[str], default=None
):  # pick 함수 선언할게 (d: 딕셔너리 입력, candidates: 문자열 리스트 입력, default: 아무 키도 못 찾으면 반환할 기본값, 따로 지정 안 하면 None)
    """여러 후보 키 중 첫 번째로 존재하는 값을 반환"""
    for (
        k
    ) in (
        candidates
    ):  # candidates 리스트에서 키(k)를 하나씩 꺼내서 순서대로 확인하는 반복문 실행
        if k in d and d[k] not in (
            None,
            "",
        ):  # 딕셔너리 d에 키 k가 존재하고, 그 값이 None이나 빈 문자열("")이 아닐 때만
            return d[k]  # 조건을 만족한 첫 번째 키의 값을 반환하고 함수 종료
    return default  # candidates 중 유효한 키를 못 찾으면 기본값(default)을 반환해줘


def make_doc_id(name: str, description: str, source: str = "") -> str:
    # name, description, source를 조합해서 고유한 ID 문자열을 만들어 반환하는 make_doc_id 함수 선언할게
    # (name: 문자열 입력, description: 문자열 입력, source: 문자열 입력 / 값 없으면 빈 문자열로 기본값 설정, -> str: 결과값은 문자열로 반환)
    """doc_id가 없을 때 임시로 만들기(내용 기반 해시)"""
    raw = f"{source}||{name}||{description}".encode("utf-8")
    # source, name, description을 || 구분자로 연결한 뒤, 해시 처리를 위해 utf-8 방식의 바이트로 변환해서 raw 변수에 저장해줘
    return hashlib.sha256(raw).hexdigest()[:32]
    # raw 바이트를 SHA-256 알고리즘으로 해시 변환하고, 16진수 문자열로 꺼낸 뒤 앞 32글자만 잘라서 doc_id로 반환해줘


class Command(
    BaseCommand
):  # BaseCommand(명령어 기본 틀)을 기반으로 Command 클래스 생성할게
    help = "Import collected reviews from CSV or JSONL into DB."  # help 변수에 문자열 담아줘

    def add_arguments(
        self, parser
    ):  # # 터미널에서 명령어 실행 시 옵션값을 입력받는 add_arguments 함수 선언할게
        parser.add_argument(
            "--path",  # 터미널에서 --path 로 입력받을게
            required=True,  # 필수 입력값이야, 없으면 오류 발생해
            help="data file path (csv/jsonl)",  # --help 실행 시 보여줄 설명이야
        )
        parser.add_argument(
            "--source",  # 터미널에서 --source 로 입력받을게
            default="",  # 입력 안 하면 빈 문자열("")을 기본값으로 사용할게
            help="source name e.g. naver/musinsa",  # --help 실행 시 보여줄 설명이야
        )
        parser.add_argument(
            "--limit",  # 터미널에서 --limit 으로 입력받을게
            type=int,  # 입력값을 정수형으로 변환해서 받을게
            default=0,  # 입력 안 하면 0을 기본값으로 사용할게 (0이면 전체 처리)
            help="limit rows for test (0=all)",  # --help 실행 시 보여줄 설명이야
        )
        parser.add_argument(
            "--batch",  # 터미널에서 --batch 로 입력받을게
            type=int,  # 입력값을 정수형으로 변환해서 받을게
            default=1000,  # 입력 안 하면 1000을 기본값으로 사용할게
            help="bulk_create batch size",  # --help 실행 시 보여줄 설명이야
        )

    def handle(self, *args, **options):
        # 명령어 실행 시 핵심 로직을 처리하는 handle 함수 선언할게
        # (*args: 추가 위치 인자 묶음, **options: 터미널에서 입력한 --path, --source 등 옵션값 묶음)

        path = Path(options["path"])
        # 터미널에서 입력한 --path 값을 Path 객체로 변환해서 path 변수에 담아줘 (파일 존재 여부 확인 등에 활용)

        source = options["source"].strip()
        # 터미널에서 입력한 --source 값의 앞뒤 공백을 제거해서 source 변수에 담아줘

        limit = options["limit"]
        # 터미널에서 입력한 --limit 값을 limit 변수에 담아줘 (0이면 전체 처리, 숫자면 해당 행 수만큼만 처리)

        batch_size = options["batch"]
        # 터미널에서 입력한 --batch 값을 batch_size 변수에 담아줘 (한 번에 DB에 저장할 행 수)

        if not path.exists():
            # 입력한 경로에 파일이 실제로 존재하지 않으면
            raise CommandError(f"File not found: {path}")
            # CommandError로 "File not found: {경로}" 오류 메시지를 띄우고 실행을 중단해줘

        suffix = path.suffix.lower()
        # 파일 확장자를 소문자로 변환해서 suffix 변수에 담아줘 (예: ".CSV" → ".csv")

        if suffix not in [".csv", ".jsonl"]:
            # 확장자가 .csv도 .jsonl도 아니면
            raise CommandError("Only .csv or .jsonl is supported")
            # CommandError로 "csv와 jsonl만 지원한다" 오류 메시지를 띄우고 실행을 중단해줘

        if suffix == ".csv":
            # 확장자가 .csv이면
            rows = self._read_csv(path, limit=limit)
            # _read_csv 함수로 파일을 읽어서 rows 변수에 담아줘
        else:
            # .csv가 아니면 (.jsonl이면)
            rows = self._read_jsonl(path, limit=limit)
            # _read_jsonl 함수로 파일을 읽어서 rows 변수에 담아줘

        total = len(rows)
        # rows의 전체 행 수를 세서 total 변수에 담아줘

        self.stdout.write(self.style.NOTICE(f"Loaded {total} rows from {path.name}"))
        # 터미널에 "파일명에서 몇 행을 불러왔다"는 안내 메시지를 출력해줘

        to_create = []
        # DB에 저장할 객체들을 담아둘 빈 리스트 to_create 만들어줘

        for r in rows:
            # rows에서 행(r)을 하나씩 꺼내서 순서대로 처리하는 반복문 실행

            # ---- 컬럼 매핑(너 데이터에 맞게 후보 키를 늘릴 수 있음) ----

            name = pick(r, ["name", "title", "subject"], default="(no title)")
            # pick 함수로 r에서 name, title, subject 순서로 값을 찾아서 name 변수에 담아줘
            # 아무것도 없으면 "(no title)"을 기본값으로 사용할게

            description = pick(
                r, ["description", "text", "content", "review"], default=""
            )
            # pick 함수로 r에서 description, text, content, review 순서로 값을 찾아서 description 변수에 담아줘
            # 아무것도 없으면 빈 문자열을 기본값으로 사용할게

            doc_id = pick(r, ["doc_id", "id", "document_id", "uuid"], default=None)
            # pick 함수로 r에서 doc_id, id, document_id, uuid 순서로 값을 찾아서 doc_id 변수에 담아줘
            # 아무것도 없으면 None을 기본값으로 사용할게

            if not doc_id:
                # doc_id 값이 없으면 (None이면)
                doc_id = make_doc_id(name, description, source=source)
                # make_doc_id 함수로 name, description, source를 해싱해서 임시 doc_id를 생성해줘

            collected_at_raw = pick(
                r, ["collected_at", "created_at", "date", "datetime"], default=None
            )
            # pick 함수로 r에서 collected_at, created_at, date, datetime 순서로 날짜값을 찾아서
            # collected_at_raw 변수에 담아줘. 아무것도 없으면 None을 기본값으로 사용할게

            collected_at = None
            # 최종적으로 저장할 날짜값 변수 collected_at을 None으로 초기화해줘

            if collected_at_raw:
                # collected_at_raw에 값이 있으면

                if isinstance(collected_at_raw, str):
                    # 그 값이 문자열 형태이면

                    collected_at = parse_datetime(collected_at_raw)
                    # parse_datetime 함수로 문자열을 Django가 인식하는 datetime 형식으로 변환해서
                    # collected_at 변수에 담아줘

                    if collected_at is None:
                        # parse_datetime 변환에 실패해서 여전히 None이면 (날짜만 있는 경우 등)

                        try:
                            collected_at = datetime.fromisoformat(collected_at_raw)
                            # 파이썬 내장 fromisoformat 함수로 한 번 더 변환 시도해줘
                        except Exception:
                            collected_at = None
                            # 그것도 실패하면 None으로 그냥 넘어가줘

            obj = CollectedReview(
                # 위에서 정리한 값들로 CollectedReview 객체를 만들어줘 (아직 DB 저장 전 상태)
                doc_id=str(doc_id),  # doc_id는 문자열로 변환해서 담아줘
                name=str(name)[
                    :255
                ],  # name은 문자열로 변환하고 255자까지만 잘라서 담아줘
                description=str(description),  # description은 문자열로 변환해서 담아줘
                source=source,  # 터미널에서 입력한 source 값 담아줘
                collected_at=collected_at,  # 변환된 날짜값 담아줘
            )
            to_create.append(obj)
            # 만든 객체를 to_create 리스트에 추가해줘

        # ---- DB 적재 ----

        created_count = 0
        # 저장된 행 수를 세기 위한 카운터 변수 created_count를 0으로 초기화해줘

        for i in range(0, len(to_create), batch_size):
            # to_create 리스트를 batch_size 간격으로 나눠서 순서대로 처리하는 반복문 실행
            # 예: batch_size=1000이면 0~999, 1000~1999, 2000~2999 순서로 처리

            chunk = to_create[i : i + batch_size]
            # to_create에서 현재 배치 범위만큼 잘라서 chunk 변수에 담아줘

            # ignore_conflicts=True => unique(doc_id) 충돌이면 자동 스킵(PostgreSQL 권장)
            CollectedReview.objects.bulk_create(
                chunk, ignore_conflicts=True, batch_size=batch_size
            )
            # chunk에 담긴 객체들을 한 번에 DB에 저장해줘
            # 이미 같은 doc_id가 DB에 있으면 오류 없이 자동으로 건너뛰어줘 (중복 방지)

            created_count += len(chunk)
            # 이번 배치에서 처리한 행 수를 created_count에 누적해줘

            self.stdout.write(f"Inserted batch: {i} ~ {i + len(chunk) - 1}")
            # 터미널에 현재 배치의 처리 범위를 출력해줘 (예: "Inserted batch: 0 ~ 999")

        self.stdout.write(
            self.style.SUCCESS("Done. (Duplicates skipped by doc_id unique)")
        )
        # 터미널에 "완료, 중복된 doc_id는 건너뜀" 성공 메시지를 초록색으로 출력해줘

    def _read_csv(self, path: Path, limit: int = 0) -> list[dict]:
        # CSV 파일을 읽어서 각 행을 딕셔너리로 변환한 리스트를 반환하는 _read_csv 함수 선언할게
        # (path: 읽을 파일 경로, limit: 읽을 최대 행 수 / 0이면 전체 읽기, -> list[dict]: 결과값은 딕셔너리 리스트로 반환)

        # UTF-8 BOM 대응: utf-8-sig
        # 엑셀 등에서 저장한 CSV에 BOM 문자가 포함될 수 있어서 utf-8-sig 방식으로 자동 제거할게

        data = []
        # 읽어온 행들을 담아둘 빈 리스트 data 만들어줘

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            # path 경로의 파일을 읽기 모드("r")로 열어줘
            # (encoding="utf-8-sig": BOM 자동 제거, newline="": 줄바꿈 문자를 csv 모듈이 직접 처리하게 해줘)

            reader = csv.DictReader(f)
            # csv.DictReader로 파일을 읽어줘
            # (첫 번째 행을 헤더로 인식해서 각 행을 {컬럼명: 값} 형태의 딕셔너리로 변환해줘)

            for idx, row in enumerate(reader):
                # reader에서 행(row)을 하나씩 꺼내면서 순서 번호(idx)도 같이 추적하는 반복문 실행

                data.append(row)
                # 읽어온 행을 data 리스트에 추가해줘

                if limit and (idx + 1) >= limit:
                    # limit이 0이 아니고, 지금까지 읽은 행 수(idx + 1)가 limit에 도달하면
                    # (idx는 0부터 시작해서 +1로 실제 행 수를 계산)

                    break
                    # 반복문을 종료하고 더 이상 읽지 마줘

        return data
        # 읽어온 행들이 담긴 data 리스트를 반환해줘

    def _read_jsonl(self, path: Path, limit: int = 0) -> list[dict]:
        # JSONL 파일을 읽어서 각 줄을 딕셔너리로 변환한 리스트를 반환하는 _read_jsonl 함수 선언할게
        # (path: 읽을 파일 경로, limit: 읽을 최대 행 수 / 0이면 전체 읽기, -> list[dict]: 결과값은 딕셔너리 리스트로 반환)

        data = []
        # 읽어온 행들을 담아둘 빈 리스트 data 만들어줘

        with path.open("r", encoding="utf-8") as f:
            # path 경로의 파일을 읽기 모드("r")로 열어줘
            # (encoding="utf-8": utf-8 방식으로 읽을게)

            for idx, line in enumerate(f):
                # 파일에서 줄(line)을 하나씩 꺼내면서 순서 번호(idx)도 같이 추적하는 반복문 실행

                line = line.strip()
                # 줄 앞뒤의 공백이나 줄바꿈 문자를 제거해서 line 변수에 다시 담아줘

                if not line:
                    # 공백 제거 후 빈 줄이면
                    continue
                    # 이 줄은 건너뛰고 다음 줄로 넘어가줘

                data.append(json.loads(line))
                # json.loads로 현재 줄의 JSON 문자열을 딕셔너리로 변환해서 data 리스트에 추가해줘

                if limit and (idx + 1) >= limit:
                    # limit이 0이 아니고, 지금까지 읽은 행 수(idx + 1)가 limit에 도달하면

                    break
                    # 반복문을 종료하고 더 이상 읽지 마줘

        return data
        # 읽어온 행들이 담긴 data 리스트를 반환해줘
