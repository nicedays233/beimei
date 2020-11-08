import redis

if __name__ == '__main__':
    handler = redis.Redis(host="192.168.56.101",port=6379, decode_responses=True)
    print(handler.get("jyx"))
