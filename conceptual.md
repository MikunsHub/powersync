# 1a(i)
What pros and cons do you see with respect to obtaining readings from an MQTT broker, vs getting them via a REST API?


| Aspect              | MQTT Broker                                            | REST API                                                |
|---------------------|--------------------------------------------------------|---------------------------------------------------------|
| **Scalability**     | They are ideal for real-time data streaming and high volumes.  | Suitable for smaller data sets and occasional requests. |
| **Efficiency**      | Low overhead due to the lightweight pub/sub architecture.   | May have higher overhead due to request/response model. |
| **Real-time**       | Provides real-time data updates for subscribers due to the fact that it has high latency     | May introduce latency depending on server response.    |
| **Connection**      | Persistent connection to broker, efficient for IoT applications.  | Requires a new connection for each API request.       |
| **Bandwidth**       | Efficient for low-bandwidth and intermittent networks.| May require more bandwidth due to repeated requests.  |
| **Complexity**      | The Publish/subscribe model can be more complex to set up.| The request/response model is easier to understand. |

MQTT's push-based, stateful nature makes it a better choice for real-time data streaming and scenarios with high data volumes and frequent updates.

# 1a(ii)
How would you run an acquisition function that subscribes to an MQTT broker? For example would you trigger it periodically via a scheduler, or would you have it running as some sort of continuous "listener" function?

Choosing the right method to run the acquisition function that subscribes to an MQTT broker largely depends on the specification of the application as well as the time sensitivity of the data. 

For systems(device pushing data to the broker) that require realtime updates due to Operational insights, predictive analysis, regulatory compliance and immediate action systems, I will opt for the *Continous Listening* method. The major cons of using this methods include:

- Potential for high network traffic: If the data updates are frequent, continuous listening might lead to higher network usage. This trade off would require optimisation in the data processing stage.

- Maintaining a persistent connection requires more resources compared to periodic scheduling


For systems that don't require data updates that are extremely time sensitive, the *Periodic Scheduling* method is well suitable. These kind of data updates can be acquired in batches. This method makes it easy to predict resource usage and since data is fetched at intervals network traffic is reduced. The major downside is that if the intervals are too long delayed updates become a thing.

# 1a(iii)
What underlying AWS service would you run it on? E.g. EC2 vs ECS vs Lambda, etc.

Because my preferred method of acquisition is the *Continous Listening* method I would use AWS ECS (Elastic Container Service) for this task because ECS is suitable for long-running tasks and has the ability to scale up or down based on demand. Using a Lambda function is unsuitable as Lambda functions have a maximum execution time limit, which makes them unsuitable for long-running tasks like a continuous listener. ECS services can scale in a more granular way by adjusting the number of task instances independently of the number of host instances and ECS has built-in schedulers that enable you to run tasks on a schedule or in response to CloudWatch events. This can be more efficient than manually managing task scheduling on EC2 instances.

Based on the MQTT broker being used in this project, I observed that it has periods of inactivity and no data is emitted, based on this characteristics, a Periodic Scheduler Acquisition function would be very suitable for it as it would save resources.