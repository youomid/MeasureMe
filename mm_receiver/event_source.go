package main

import (
	"time"
	"fmt"
	"log"
	"sync"
	"encoding/json"
	"math/rand"
	"github.com/streadway/amqp"
	"github.com/valyala/fasthttp"
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

func gen_comp_ws(){
	var events []map[string]interface{}

	event := map[string]interface{}{
		"user": "guest",
		"date": time.Now(),
		"eventType": "WorkSessionStartedEvent",
	}

	events = append(events, event)
	fmt.Printf("%v", events)
}

func simulate(sim_type string){
	switch sim_type {
	case "complete-work-session":
		gen_comp_ws()
	case "incomplete-work-session":
	case "paused-work-session":
	case "daily-goal-progress":
	case "daily-goal-complete":
	}
}

func requestHandler(ctx *fasthttp.RequestCtx) {
	switch string(ctx.Path()) {
	case "/simulate":
		fmt.Printf("Received request\n")
		req := &ctx.Request
		fmt.Printf(string(req.Body()))

		simulate(string(req.Body()))

	}
}

func start_server(){
	h := requestHandler
	go func() {
		fmt.Printf("Server started\n")
		if err := fasthttp.ListenAndServe("127.0.0.1:6470", h); err != nil {
			fmt.Sprintf("Error in ListenAndServe: %s", err)
		}
	}()
}

func main() {
	wg.Add(1)
	// go send_sample_events(10000)
	start_server()
	wg.Wait()
}




