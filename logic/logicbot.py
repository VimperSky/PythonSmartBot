import chatterbot.comparisons
import chatterbot.response_selection

bot = chatterbot.ChatBot("200 IQ", database_uri='sqlite:///db.sqlite3', read_only=True, logic_adapters=[
    {
        'import_path': 'logic.smart_match.SmartMatch',
        "statement_comparison_function": chatterbot.comparisons.LevenshteinDistance,
        "response_selection_method": chatterbot.response_selection.get_most_rated_response,
        'default_response': 'Я ничего не понял, давай по новой?',
        'maximum_similarity_threshold': 0.99
    }]
)

print("Logic bot is running!")

def get_response(text):
    return bot.get_response(text)