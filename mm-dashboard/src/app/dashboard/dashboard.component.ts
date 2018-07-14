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
  }

  sendMessage(){
    this._api.postEvent("0 minutes ago", "Test Event", "Test Description")
  }

  getDashboard(){
    this._api.getDashboard()
  }

}
