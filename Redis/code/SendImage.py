import redis        # pip install redis
import io;

ip=""
r = redis.Redis(host=ip, port=6379, db=0,password='sofe4630u')

with open("ontarioTech.jpg", "rb") as f:
    value = f.read();
r.set('OntarioTech',value);
print('Image sent')