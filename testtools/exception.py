import content


class DetailedException(Exception):
    """
    Exception base class that supports testtools' detail mechanism.

    The Exception's name is added in a detail called "reason".
    The Exception's message is added in a detailed called "reason-detail".
    """

    def __init__(self, message, *args, **kwargs):
        """*args are assumed to be text type,
        **kwargs are assumed to be content objects"""
        super(DetailedException, self).__init__(message)
        self.__details = {}
        self.addDetail(
            'reason', content.text_content(self.__class__.__name__))
        self.addDetail(
            'reason-detail', content.text_content(message)
        )
        for arg in args:
            self.addDetail('detail', content.text_content(arg))
        for label, content in kwargs.each():
            self.addDetail(label, content)

    def addDetail(self, name, content_object):
        """Add a detail to be reported with this exception.

        For more details see pydoc testtools.TestResult.

        :param name: The name to give this detail.
        :param content_object: The content object for this detail. See
            testtools.content for more detail.
        """
        existing_details = self.getDetails()
        full_name = name
        suffix = 1
        while full_name in existing_details:
            full_name = "%s-%d" % (name, suffix)
            suffix += 1
        self.__details[full_name] = content_object

    def getDetails(self):
        """Get the details dict that will be reported with this test's outcome.

        For more details see pydoc testtools.TestResult.
        """
        return self.__details

    def _report_traceback(self, exc_info, tb_label='traceback'):
        self.addDetail(tb_label, content.TracebackContent(exc_info, self))
