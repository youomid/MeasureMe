import { Component, OnInit } from '@angular/core';
import { APIService } from './../api.service';
import { Chart } from 'chart.js';
import '../../../node_modules/rxjs/add/operator/map';


@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css']
})
export class SummaryComponent implements OnInit {

  chart = []; 

  constructor(private _api: APIService) { }

  ngOnInit() {
  	var res = this._api.testData()

    let temp_max = res['list'].map(res => res.main.temp_max);
	let temp_min = res['list'].map(res => res.main.temp_min);
	let alldates = res['list'].map(res => res.dt)

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

  }

}
