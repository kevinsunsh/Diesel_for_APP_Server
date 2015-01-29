# coding: utf8
import ujson as json
import time
from diesel.protocols.redis import RedisClient, RedisTransactionError, RedisLock, LockNotAcquired
from comment import Comment

def process(command):
    proposal_id = command['proposal_id']
    comment_index = command['comment_index']

    client = RedisClient(host='localhost', port=6391)
    client.select(2)
    #sadd
    comment_id = "comment_" + str(proposal_id)
    print comment_id
    content = client.lrange(comment_id, comment_index, comment_index)
    print content[0]
    client.lrem(comment_id, content[0], 1)

    comments = []
    comment_list = client.lrange(comment_id, 0, -1)
    for comment in comment_list:
        result = comment.split('^')
        if len(result)>=3:
            comments.append(Comment(result[0], result[1], result[2]).data_dict)
    return reply(True, command, comments)

def reply(result, command, comments):
    return{'command': command['command'], 'command_index': command['command_index'], \
            "result":result, "comments":comments}