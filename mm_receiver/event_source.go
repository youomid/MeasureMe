package main

import (
	"fmt"
	"log"
	"sync"
	"github.com/streadway/amqp"
)

/*
	This script sends sample event data to our message queue 
	and also logs each event. In the future, this script would also serve
	as an api receiving data from registered mobile applications. In total, these applications
	send thousands of events per second.

	Note: When binding a queue to the exchange, make sure to include a routing
		  key.
*/


var wg sync.WaitGroup

func failOnError(err error, msg string) {
  if err != nil {
    log.Fatalf("%s: %s", msg, err)
    panic(fmt.Sprintf("%s: %s", msg, err))
  }
}

func log_event(){
	fmt.Printf("Logging event...\n")
}

func queue_event(){
	fmt.Printf("Queuing event...\n")
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5673/")
	failOnError(err, "Failed to dial RMQ")
	ch, err := conn.Channel()
	failOnError(err, "Failed to declare a channel")
	q, err := ch.QueueDeclare(
	  "test", // name
	  true,   // durable
	  false,   // delete when unused
	  false,   // exclusive
	  false,   // no-wait
	  nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")
	body := "hello"
	err = ch.Publish(
	  "test_queue",     // exchange
	  q.Name, // routing key
	  false,  // mandatory
	  false,  // immediate
	  amqp.Publishing {
	    ContentType: "text/plain",
	    Body:        []byte(body),
	  })
	failOnError(err, "Failed to publish")
}

func send_sample_events(num_events int){

	defer wg.Done()
	for i:= 0; i < num_events; i++ {
		queue_event()
		log_event()
	}

}

func main() {
	wg.Add(1)
	go send_sample_events(50)
	wg.Wait()
}