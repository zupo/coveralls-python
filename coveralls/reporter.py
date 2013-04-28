# coding: utf-8
import logging

from coverage.report import Reporter
from coverage.misc import NoSource


log = logging.getLogger('coveralls')


class CoverallReporter(Reporter):
    """ Custom coverage.py reporter for coveralls.io
    """
    def report(self, morfs=None):
        """ Generate a part of json report for coveralls

        `morfs` is a list of modules or filenames.
        `outfile` is a file object to write the json to.
        """
        self.source_files = []
        try:
            self.report_files(self.parse_file, morfs)
        except NoSource, e:
            log.warning("Skipping a file because no source was found: {0}".format(
                e.message.replace("No source for code: ", "")))
        return self.source_files

    def get_hits(self, line_num, analysis):
        """ Source file stats for each line.

            * A positive integer if the line is covered,
            representing the number of times the line is hit during the test suite.
            * 0 if the line is not covered by the test suite.
            * null to indicate the line is not relevant to code coverage
              (it may be whitespace or a comment).
        """
        if line_num in analysis.missing:
            return 0
        if line_num in analysis.statements:
            return 1
        return None

    def parse_file(self, cu, analysis):
        """ Generate data for single file """
        filename = cu.file_locator.relative_filename(cu.filename)
        coverage_lines = [self.get_hits(i, analysis) for i in range(1, len(analysis.parser.lines) + 1)]
        self.source_files.append({
            'name': filename,
            'source': cu.source_file().read(),
            'coverage': coverage_lines
        })