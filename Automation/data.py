import wikipedia
from speech import prntdisp

def tell_me_about(topic):
    try:
        # info = str(ny.content[:500].encode('utf-8'))
        # res = re.sub('[^a-zA-Z.\d\s]', '', info)[1:]
        res = wikipedia.summary(topic, sentences=3)
        prntdisp(res)

    except Exception as e:
        print(e)
        return False
