# Assn1_DSP
## Team member
Wei Fan(wei.fan@vanderbilt.edu Github id: FWWorks)  
Dingjie Su(dingjie.su@Vanderbilt.Edu Github id: sudmat)  
Zhehao Zeng(zhehao.zeng@vanderbilt.edu Github id: frankvandy2018) 

## Project code
https://github.com/FWWorks/Assn1_DSP

## Abstract
We built a layer upon the PUB/SUB model supported by ZMQ to support anonymity between publishers and subscribers. 
To be specific, we provide two ways as to how data disseminated from publishers and subscribers. One way is, that we wrote code to support the publisher’s middleware layer directly sending the data to the subscribers who are interested in the topic being published by this publisher. Another approach allows the publisher’s middleware always send the information to the broker, who then sends it to the subscribers for this topic. 
Our team also conducted performance measurement experiments to get a sense of the impact on amount of data sent, latency of dissemination, pinpointing the source of bottlenecks.
The code is written in Python3.5 and we use Mininet to build single topologies to test our code, which runs on Linux Ubuntu.

## What we implemented
### Two approaches to data disseminating from publishers and subscribers. 
To be more specific, both for publisher’s middleware layer directly sending the data to the subscribers or for publisher’s middleware sending the information to the broker, who then sends it to the subscribers for this topic. In both ways, we provide APIs for publisher/subscriber registering the system, publisher publishing messages under topics, subscriber receive the messages which come from the topics it is interested in. 
### APIs for publishers and subscribers leaving any time. 
We realized the functions for publishers and subscribers leaving the system, publisher canceling a topic, subscribers unsubscribing a specific topic. 
### Heartbeat sending and timeout handling
A publisher or a subscriber sends heartbeat messages to the broker once it registers to be a member in the system. And if the broker haven’t received a heartbeat message from a publisher/subscriber, the broker will drop this member out from the system because there must be something wrong with the member. 

## How to run our code
![Alt text](./img/dir.png "")

## Test case

## Performance measurement
