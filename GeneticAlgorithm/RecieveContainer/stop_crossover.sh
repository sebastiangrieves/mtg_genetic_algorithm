for i in {1..10}
do
	docker stop request_$i
	docker rm request_$i
done
docker ps -a