import time 
from queue import Queue 

def main(): 
    # simulate incoming requests 
    requests = Queue(maxsize= 60 )
    for i in range(1, 61):
        requests.put(i)
        
    # this limiter function will return True every 200 millisecinds
    def limiter():
        while True:
            yield
            time.sleep(0.2)
            
    limit = limiter()
    
    #by calling next() on the limiter before serving each request,
    #we limit ourseleves to 1 request every 200 milliseconds
    while not requests.empty():
        next(limit)
        req = requests.get()
        print(f"request {req} {time.time()}")
        
    # we may want to allow short burst of requests in our rate limiting schema 
    # while preserving the overall rate mimit. we can o this by using a token bucket algorithim
    
    class TokenBucket:
        def __init__(self, tokens, fill_rate):
            self.capacity = tokens
            self.tokens = tokens
            self.fill_rate = fill_rate
            self.timestamp = time.time()
            
        def get_token(self):
            now = time.time()
            if self.tokens < self.capacity:
                self.tokens += self.fill_rate * (now - self.timestamp)
            self.timestamp = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
        
        
# this bursty_limiter will allow for bursts of upto 3 events
    busrty_limiter = TokenBucket(3, 0.2)
    
    
    # now simulate more incoming requests. the first few will benefit from,
    # the burst capabiliuty of the function
    bursty_requests = Queue(maxsize=60)
    for i in range (1, 61):
        bursty_requests.put(i)
        
    while not bursty_requests.empty():
        if busrty_limiter.get_token():
            req = bursty_requests.get()
            print(f"request {req} {time.time()}")
            
        else: 
            time.sleep(0.1)
            
if __name__ == "__main__":
    main()

        
        
