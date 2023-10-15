from dataclasses import dataclass


@dataclass
class EnglishVerbAnswer:
    infinitive: str
    past: str
    past_participle: str


@dataclass
class EnglishVerb(EnglishVerbAnswer):
    slovene_verb: str
