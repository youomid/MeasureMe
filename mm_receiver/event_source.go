package main

import (
	"fmt"
	"log"
	"sync"
	"encoding/json"
	"math/rand"
	"github.com/streadway/amqp"
)

/*
	This script sends sample event data to our message queue 
	and also logs each event. In the future, this script would also serve
	as an api receiving data from registered mobile applications. In production, this api could
	be processing thousands of events per second.
*/


var (
	channel          *amqp.Channel
	wg               sync.WaitGroup
)

func failOnError(err error, msg string) {
  if err != nil {
    log.Fatalf("%s: %s", msg, err)
    panic(fmt.Sprintf("%s: %s", msg, err))
  }
}

func log_event(event_num int){
	fmt.Printf("Logging event number: %d\n", event_num)
}

func generate_random_event() map[string]interface{} {
	minutes := rand.Intn(100)

	msg := map[string]interface{}{"user": "test_user", "date": minutes,
	"title": "Test title", "description": "test description"}

	return msg
}

func queue_event(){
	body, _ := json.Marshal(generate_random_event())
	err := channel.Publish(
	  "test_queue",  // exchange
	  "test", // routing key
	  false,  // mandatory
	  false,  // immediate
	  amqp.Publishing{
        Headers:         amqp.Table{},
        ContentType:     "application/json",
        ContentEncoding: "",
        Body:            []byte(body),
        DeliveryMode:    amqp.Transient, 
        Priority:        0,              
	  },)
	failOnError(err, "Failed to publish")
}

func send_sample_events(num_events int){
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5673/")
	failOnError(err, "Failed to dial RMQ")
	channel, err = conn.Channel()
	failOnError(err, "Failed to declare a channel")
	defer wg.Done()
	for i:= 0; i < num_events; i++ {
		queue_event()
		log_event(i)
	}

}

func main() {
	wg.Add(1)
	go send_sample_events(10000)
	wg.Wait()
}