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

func generate_random_event() map[string]interface{} {
	minutes := rand.Intn(100)

	msg := map[string]interface{}{"user": "test_user", "date": minutes,
	"title": "Test title", "description": "test description"}

	return msg
}

func current_time() int64 {
    return time.Now().UnixNano() / (int64(time.Millisecond)/int64(time.Nanosecond))
}

func gen_comp_ws() []map[string]interface{} {
	// generate complete work session events

	var events []map[string]interface{}

	current := current_time()

	event := map[string]interface{}{
		"user": "guest",
		"date": current,
		"eventType": "WorkSessionStartedEvent",
	}
	event["eventInfo"] = map[string]interface{}{
		"SessionLength": 25,
	}
	events = append(events, event)

	// work session is completed after 25 minutes
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 1500000,
		"eventType": "WorkSessionCompletedEvent",
	}
	events = append(events, event)

	event = map[string]interface{}{
		"user": "guest",
		"date": current + 1500000,
		"eventType": "BreakSessionStartedEvent",
	}
	event["eventInfo"] = map[string]interface{}{
		"SessionLength": 5,
	}
	events = append(events, event)

	// break session is completed after 5 minutes
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 300000,
		"eventType": "BreakSessionCompletedEvent",
	}
	events = append(events, event)

	return events
}

func simulate(sim_type string){
	var events []map[string]interface{}
	switch sim_type {
	case "complete-work-session":
		events = gen_comp_ws()
	case "incomplete-work-session":
	case "paused-work-session":
	case "daily-goal-progress":
	case "daily-goal-complete":
	}
	publish_events(events)
}

func publish_events(events []map[string]interface{}){
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5673/")
	failOnError(err, "Failed to dial RMQ")

	channel, err = conn.Channel()
	failOnError(err, "Failed to declare a channel")

	for _, element := range events {
		body, _ := json.Marshal(element)
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




