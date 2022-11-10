for i in {1..10}
do
	docker run -d -e RABBIT_HOST=10.30.2.244 -e QUEUE_NAME=hello -e QUEUE_SEND_NAME=hello_recieve --name request_$i request
done
docker ps -a
