import { Component, OnInit } from '@angular/core';
import { APIService } from './../api.service';
import { Chart } from 'chart.js';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  chart = []; 
  socket = new WebSocket("ws://" + 'localhost:8000' + "/events/");
  events = [];
  columnNames = ["Date", "Complete Work Sessions", "Incomplete Work Sessions", "Paused Work Sessions", "Daily Complete", "Complete Break Session", "Earned Break Points", "Consumed Break Points"]
  columnValues = [["July 17th, 2018", 6,2,1,1,3,700,150],["July 18th, 2018", 6,2,1,1,3,700,150],["July 19th, 2018", 6,2,1,1,3,700,150]]

  constructor(private _api: APIService) { }

  ngOnInit() {
  	var res = this._api.testData()

    let temp_max = res['list'].map(res => res.main.temp_max);
  	let temp_min = res['list'].map(res => res.main.temp_min);
  	let alldates = res['list'].map(res => res.dt);

  	let weatherDates = []
  	
  	alldates.forEach((res) => {
  	    let jsdate = new Date(res * 1000)
  	    weatherDates.push(jsdate.toLocaleTimeString('en', { year: 'numeric', month: 'short', day: 'numeric' }))
  	})

  	var ctx = document.getElementById("myChart");
  	var chartData = {
        type: 'line',
        data: {
          labels: weatherDates,
          datasets: [
            { 
              data: temp_max,
              borderColor: "#3cba9f",
              fill: false
            },
            { 
              data: temp_min,
              borderColor: "#ffcc00",
              fill: false
            },
          ]
        },
        options: {
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              display: true
            }],
            yAxes: [{
              display: true
            }],
          }
        }
      };

    	this.chart = new Chart(ctx, chartData);

      let localSocket = this.socket;

      var self = this;

      this.socket.onmessage = function(e) {
        console.log('message', e);
          var parsedData = JSON.parse(e.data);
          self.events.push(parsedData)
      }

      this.events = [
        {'date': '27 Minutes Ago', 'title': 'Started work session', 'description': 'Studying for finals'},
        {'date': '15 Minutes Ago', 'title': 'Paused work session', 'description': 'Studying for finals'},
        {'date': '2 Minutes Ago', 'title': 'Finished work session', 'description': 'Studying for finals'},
      ]
      this.getDashboard()

  }

  sendMessage(){
    this._api.postEvent("0 minutes ago", "Test Event", "Test Description")
  }

  getDashboard(){
    this._api.getDashboard()
  }

  simulateCompleteWorkSession(){
    this._api.simulateCompleteWorkSession()
  }

  simulateInCompleteWorkSession(){
    this._api.simulateInCompleteWorkSession()
  }

  simulatePausedWorkSession(){
    this._api.simulatePausedWorkSession()
  }

  simulateDailyComplete(){
    this._api.simulateDailyComplete()
  }


}
