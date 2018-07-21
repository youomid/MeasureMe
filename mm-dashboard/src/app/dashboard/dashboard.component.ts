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
  columnIds = [
    'start_time', 'end_time', 'comp_ws', 'incomp_ws',
    'pws', 'daily_c', 'comp_bs', 'earned_bp', 'consumed_bp'
    ]
  columnNames = {
    "start_time":"Start Time",
    "end_time":"End Time",
    "comp_ws":"Complete Work Sessions",
    "incomp_ws":"Incomplete Work Sessions",
    "pws":"Paused Work Sessions",
    "daily_c":"Daily Complete",
    "comp_bs":"Complete Break Session",
    "earned_bp":"Earned Break Points",
    "consumed_bp":"Consumed Break Points"
    }

    daily_history = []
    monthly_history = []

  constructor(private _api: APIService) { }

  ngOnInit() {
  	var res = this._api.testData()

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

  loadChart(){
    var ctx = document.getElementById("myChart");
    var chartData = {
        type: 'line',
        data: {
          labels: this.monthly_history['start_time'],
          datasets: [
            { 
              label: "Complete Work Sessions"
              data: this.monthly_history['comp_ws'],
              borderColor: "#3cba9f",
              fill: false
            },
            { 
              label: "Inomplete Work Sessions"
              data: this.monthly_history['incomp_ws'],
              borderColor: "#ffcc00",
              fill: false
            },
            { 
              label: "Paused Work Sessions"
              data: this.monthly_history['incomp_ws'],
              borderColor: "#e55a76",
              fill: false
            },
            { 
              label: "Daily Complete"
              data: this.monthly_history['daily_c'],
              borderColor: "#c39797",
              fill: false
            },
            { 
              label: "Complete Break Session"
              data: this.monthly_history['comp_bs'],
              borderColor: "#cc0000",
              fill: false
            },
            { 
              label: "Earned Break Points"
              data: this.monthly_history['earned_bp'],
              borderColor: "#c71585",
              fill: false
            },
            { 
              label: "Consumed Break Points"
              data: this.monthly_history['consumed_bp'],
              borderColor: "#e6e6fa",
              fill: false
            }
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

  }

  getDashboard(){
    this._api.getDashboard()
      .subscribe(
          res => {
            console.log(res);
            this.daily_history = res['daily_history']
            this.monthly_history = res['monthly_history']
            // this.events = res.events
            this.loadChart()
          },
          err => {
            console.log("Error occured", err);
          }
        );
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
