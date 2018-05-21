import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import '../../node_modules/rxjs/add/operator/map';

@Injectable()
export class APIService {

  constructor(private _http: HttpClient) { }

  testData() {

    // return this._http.get("http://samples.openweathermap.org/data/2.5/history/city?q=Warren,OH&appid=b6907d289e10d714a6e88b30761fae22")
    //   .map(result => result);

    return {"message":"","cod":"200","city_id":2643743,"calctime":0.0875,"cnt":3,"list":[{"main":{"temp":279.946,"temp_min":279.946,"temp_max":279.946,"pressure":1016.76,"sea_level":1024.45,"grnd_level":1016.76,"humidity":100},"wind":{"speed":4.59,"deg":163.001},"clouds":{"all":92},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"rain":{"3h":2.69},"dt":1485717216},{"main":{"temp":282.597,"temp_min":282.597,"temp_max":282.597,"pressure":1012.12,"sea_level":1019.71,"grnd_level":1012.12,"humidity":98},"wind":{"speed":4.04,"deg":226},"clouds":{"all":92},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"rain":{"3h":0.405},"dt":1485745061},{"main":{"temp":279.38,"pressure":1011,"humidity":93,"temp_min":278.15,"temp_max":280.15},"wind":{"speed":2.6,"deg":30},"clouds":{"all":90},"weather":[{"id":701,"main":"Mist","description":"mist","icon":"50d"},{"id":741,"main":"Fog","description":"fog","icon":"50d"}],"dt":1485768552}]}
  }

}
