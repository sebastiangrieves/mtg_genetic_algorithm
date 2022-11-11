for i in {1..10}
do
	docker run -d -e RABBIT_HOST=10.40.1.34 -e QUEUE_NAME=games --name request_$i request
done
docker ps -a
