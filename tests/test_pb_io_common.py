import logging

from base_utils import get_temp_file
from pbcommand.pb_io import load_pipeline_chunks_from_json, write_pipeline_chunks
from pbcommand.models import PipelineChunk
from pbcommand.testkit.base_utils import get_temp_dir

log = logging.getLogger(__name__)


class TestWriteChunk:

    def test_write_chunks(self):

        def f(i):
            return {"{c}movie_fofn_id".format(c=PipelineChunk.CHUNK_KEY_PREFIX): "/path/to_movie-{i}.fofn".format(i=i),
                    "{c}region_fofn_id".format(c=PipelineChunk.CHUNK_KEY_PREFIX): "/path/rgn_{i}.fofn".format(i=i)}

        def to_i(i): return "chunk-id-{i}".format(i=i)
        def to_p(i): return PipelineChunk(to_i(i), **f(i))

        nchunks = 5
        pipeline_chunks = [to_p(i) for i in range(nchunks)]
        log.debug(pipeline_chunks)
        tmp_dir = get_temp_dir("pipeline-chunks")
        tmp_name = get_temp_file("_chunk.json", tmp_dir)

        write_pipeline_chunks(pipeline_chunks, tmp_name, "Example chunk file")

        pchunks = load_pipeline_chunks_from_json(tmp_name)
        assert len(pchunks) == nchunks
