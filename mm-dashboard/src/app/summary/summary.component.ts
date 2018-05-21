import { Component, OnInit } from '@angular/core';
import { APIService } from './../api.service';
import { Chart } from 'chart.js';


@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css']
})
export class SummaryComponent implements OnInit {

  chart = []; 

  constructor(private _api: APIService) { }

  ngOnInit() {
  	this._api.testData()
      .subscribe(res => {
        console.log(res)
      })

  }

}
