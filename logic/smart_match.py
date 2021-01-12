from chatterbot.logic import LogicAdapter
from chatterbot import filters

from logic import alternative_response_provider
from logic.smart_search import SmartSearch

class SmartMatch(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.excluded_words = kwargs.get('excluded_words')
        self.smart_search = SmartSearch(chatbot)


    def can_process(self, statement):
        return True


    def use_response(self, input_statement, closest_match, additional_response_selection_parameters):
        self.chatbot.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
            closest_match.text, input_statement.text, closest_match.confidence
        ))

        recent_repeated_responses = filters.get_recent_repeated_responses(
            self.chatbot,
            input_statement.conversation
        )

        for index, recent_repeated_response in enumerate(recent_repeated_responses):
            self.chatbot.logger.info('{}. Excluding recent repeated response of "{}"'.format(
                index, recent_repeated_response
            ))

        response_selection_parameters = {
            'search_in_response_to': closest_match.search_text,
            'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words
        }

        alternate_response_selection_parameters = {
            'search_in_response_to': self.chatbot.storage.tagger.get_bigram_pair_string(
                input_statement.text
            ),
            'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words
        }

        if additional_response_selection_parameters:
            response_selection_parameters.update(additional_response_selection_parameters)
            alternate_response_selection_parameters.update(additional_response_selection_parameters)

        # Get all statements that are in response to the closest match
        response_list = list(self.chatbot.storage.filter(**response_selection_parameters))
        response_list.insert(0, closest_match)

        alternate_response_list = []

        if not response_list:
            self.chatbot.logger.info('No responses found. Generating alternate response list.')
            alternate_response_list = list(self.chatbot.storage.filter(**alternate_response_selection_parameters))

        if response_list:
            self.chatbot.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )

            response = self.select_response(
                input_statement,
                response_list,
                self.chatbot.storage
            )
            with open('responses.txt', "w", encoding="utf-8") as f:
                for resp in response_list:
                    f.write(resp.text + '\n')


            response.confidence = closest_match.confidence
            self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))
            return response
        elif alternate_response_list:
            '''
            The case where there was no responses returned for the selected match
            but a value exists for the statement the match is in response to.
            '''
            self.chatbot.logger.info(
                'Selecting response from {} optimal alternate responses.'.format(
                    len(alternate_response_list)
                )
            )
            response = self.select_response(
                input_statement,
                alternate_response_list,
                self.chatbot.storage
            )

            response.confidence = closest_match.confidence
            self.chatbot.logger.info('Alternate response selected. Using "{}"'.format(response.text))
            return response
        else:
            return None


    def process(self, input_statement, additional_response_selection_parameters=None):
        search_results = self.smart_search.search(input_statement)
        # Use the input statement as the closest match if no other results are found

        found_results = []
        for result in search_results:
            if result is None:
                print('Force search stop due to long search time!')
                break

            found_results.append(result)

            if result.confidence >= self.maximum_similarity_threshold:
                break

        response = None
        while len(found_results) > 0 and response is None:
            use_match = found_results.pop()
            response = self.use_response(input_statement, use_match, additional_response_selection_parameters)

        if response is None:
            response = alternative_response_provider.get_response(input_statement)

        return response