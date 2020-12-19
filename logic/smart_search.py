
class SmartSearch:
    """
    :param statement_comparison_function: A comparison class.
        Defaults to ``LevenshteinDistance``.
    :param search_page_size:
        The maximum number of records to load into memory at a time when searching.
        Defaults to 1000
    """

    name = 'indexed_text_search'

    def __init__(self, chatbot, **kwargs):
        from chatterbot.comparisons import LevenshteinDistance

        self.chatbot = chatbot

        statement_comparison_function = kwargs.get(
            'statement_comparison_function',
            LevenshteinDistance
        )

        self.compare_statements = statement_comparison_function()

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

        self.max_db_search = 10000

    def search(self, input_statement, max_db_count=None, **additional_parameters):
        self.chatbot.logger.info('Beginning search for close text match')

        input_search_text = input_statement.search_text

        if not input_statement.search_text:
            self.chatbot.logger.warn(
                'No value for search_text was available on the provided input'
            )

            input_search_text = self.chatbot.storage.tagger.get_text_index_string(
                input_statement.text
            )

        search_parameters = {
            'search_text_contains': input_search_text,
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        statement_list = self.chatbot.storage.filter(**search_parameters)

        best_confidence_so_far = 0

        self.chatbot.logger.info('Processing search results')

        tries_count = 0
        # Find the closest matching known statement
        for statement in statement_list:
            tries_count += 1
            if (tries_count > self.max_db_search):
                yield None

            confidence = self.compare_statements(input_statement, statement)

            if confidence > best_confidence_so_far:
                best_confidence_so_far = confidence
                statement.confidence = confidence

                self.chatbot.logger.info('Similar text found: {} {}'.format(
                    statement.text, confidence
                ))

                yield statement