from dataclasses import dataclass, field

@dataclass
class Record:
    id: str = ''
    user_name: str = ''
    user_description: str = ''
    segment_labels: list[str] = field(default_factory=list)


def record_to_json(record: Record) -> dict:
    return {
        'id': record.id,
        'user': {
            'name': record.user_name,
            'description': record.user_description
        },
        'labels': {
            'segment': record.segment_labels
        }
    }


