from yargy import (
    Parser,
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact, attribute
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized, gram
)
COD = fact(
      'Codex',
      ['n0', 'point', 'n1', 'subpoint', 'n2', 'part', 'n3', 'article', 'n4', 'par', 'n5',
       'subsection', 'n6', 'section', 'n7', 'chapter', 'n8', 'type', 'codex']
)

COURT_ = fact(
    'Court',
    ['smth', 'type', 'court', 'rf']
)

NUM = and_(gte(1), lte(10000))

NUMBERS = rule(NUM,
               rule(eq('.').optional(), NUM).repeatable().optional())


CODEX = rule(
        or_(rule(normalized('пункт')),
            rule('п', eq('.').optional())
        ).repeatable().optional().interpretation(COD.point),

        NUMBERS.repeatable().optional().interpretation(COD.n1),

        or_(rule(normalized('подпункт')),
            rule('пп', eq('.').optional())
        ).repeatable().optional().interpretation(COD.subpoint),

        NUMBERS.repeatable().optional().interpretation(COD.n2),

        or_(rule(normalized('часть')),
            rule('ч', eq('.').optional())
        ).repeatable().optional().interpretation(COD.part),

        NUMBERS.repeatable().optional().interpretation(COD.n3),

        or_(rule(normalized('статья')),
            rule('ст', eq('.').optional())
            ).repeatable().optional().interpretation(COD.article),

        NUMBERS.repeatable().optional().interpretation(COD.n4),

        rule(normalized('параграф')).repeatable().optional().interpretation(COD.par),

        NUMBERS.repeatable().optional().interpretation(COD.n5),

        rule(normalized('подраздел')).repeatable().optional().interpretation(COD.subsection),

        NUMBERS.repeatable().optional().interpretation(COD.n6),

        rule(normalized('раздел')).repeatable().optional().interpretation(COD.section),

        NUMBERS.repeatable().optional().interpretation(COD.n7),

        rule(normalized('глава')).repeatable().optional().interpretation(COD.chapter),

        NUMBERS.repeatable().optional().interpretation(COD.n8),

        gram('ADJF').repeatable().interpretation(COD.type),

        morph_pipeline({
            'гк',
            'нк',
            'тк',
            'ук',
            'гпк',
            'упк',
            'апк',
            'жк',
            'ск',
            'уик',
            'кодекс'
        }).interpretation(COD.codex.const('Кодекс'))
     ).interpretation(COD)

COURT = rule(
        gram('NOUN').repeatable().optional().interpretation(COURT_.smth),
        gram('ADJF').repeatable().interpretation(COURT_.type),
        morph_pipeline({
            'кс',
            'вс',
            'вас',
            'суд'
        }).interpretation(COURT_.court),
        morph_pipeline({
            'рф',
            'российская федерация'
        }).interpretation(COURT_.rf),
     ).interpretation(COURT_)
