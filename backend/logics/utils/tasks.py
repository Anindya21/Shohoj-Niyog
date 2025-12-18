from celery import shared_task
from functools import lru_cache
from logics.graph.builder import build_candidate_graph


@lru_cache(maxsize=1)
def get_candidate_graph():
    return build_candidate_graph()


@shared_task(bind=True)
def run_candidate_graph(self, inputs):
    graph = get_candidate_graph()
    result = graph.invoke(inputs)
    return result
