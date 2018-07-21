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

func gen_incomp_ws() []map[string]interface{} {
	// generate incomplete work session events

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

	// work session is paused after 10 minutes
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 600000,
		"eventType": "WorkSessionPausedEvent",
	}
	events = append(events, event)

	// work session is reset after two seconds
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 602000,
		"eventType": "WorkSessionResetEvent",
	}
	events = append(events, event)

	return events
}

func gen_comp_pws() []map[string]interface{} {
	// generate complete work session event that is paused

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

	// work session is paused after 10 minutes
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 600000,
		"eventType": "WorkSessionPausedEvent",
	}
	events = append(events, event)

	// work session is restarted after 5 minutes
	event = map[string]interface{}{
		"user": "guest",
		"date": current + 900000,
		"eventType": "WorkSessionRestartedEvent",
	}
	events = append(events, event)

	// work session is completed after another 10 minutes
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

func gen_daily_p() []map[string]interface{} {
	// generate events for progress in daily goals

	var events []map[string]interface{}

	current := current_time()

	event := map[string]interface{}{
		"user": "guest",
		"date": current,
		"eventType": "DailyGoalProgressEvent",
	}
	event["eventInfo"] = map[string]interface{}{
		"Progress": 33.3,
	}
	events = append(events, event)

	return events
}

func gen_daily_c() []map[string]interface{} {
	// generate complete work session event that is paused

	var events []map[string]interface{}

	current := current_time()

	event := map[string]interface{}{
		"user": "guest",
		"date": current,
		"eventType": "DailyGoalCompletedEvent",
	}
	events = append(events, event)

	return events
}

func simulate(sim_type string){
	var events []map[string]interface{}
	switch sim_type {
	case "complete-work-session":
		fmt.Printf("complete-work-session\n")
		events = gen_comp_ws()
	case "incomplete-work-session":
		fmt.Printf("incomplete-work-session\n")
		events = gen_incomp_ws()
	case "paused-work-session":
		fmt.Printf("paused-work-session\n")
		events = gen_comp_pws()
	case "daily-goal-progress":
		fmt.Printf("daily-goal-progress\n")
		events = gen_daily_p()
	case "daily-goal-complete":
		fmt.Printf("daily-goal-complete\n")
		events = gen_daily_c()
	}
	publish_events(events)
}

func publish_events(events []map[string]interface{}){
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
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
		req := &ctx.Request
		simulate(string(req.Body()))

	}
}

func start_server(){
	h := requestHandler
	go func() {
		fmt.Printf("Server started\n")
		if err := fasthttp.ListenAndServe(":6470", h); err != nil {
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




