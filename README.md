## Version
python 3.7.0
rasa 2.8.2
## Setup
Create Env: python -m venv env


python -m venv env
.\env\Scripts\activate


## template base run in class 
class action_size(Action):
    def name(self) -> Text:
        return "action_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            return []


## run local web
rasa run actions
python -m http.server 
rasa run -m models --enable-api --cors "*" --debug
