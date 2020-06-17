import {
  throwError as observableThrowError,
  Observable,
  BehaviorSubject,
  Subject,
} from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import {
  IEnums,
  IDataScientistFilter,
  IDataScientistStats,
} from '../interfaces';
import { tap, catchError } from 'rxjs/operators';
import { SyncRequestClient } from 'ts-sync-request/dist';

@Injectable()
export class DataScientistService {
  //private getStats = "http://localhost:8070/stats";
  //private getStatsJSON = "../../assets/stat.json"
  private postFilterLink = 'http://localhost:8070/datascientist';

  private getEnumJSON = '../../assets/enum.json';

  constructor(private http: HttpClient) {}

  statsFromDataScientist: any;

  statChanged: Subject<any> = new Subject<any>();

  getEnums() {
    return this.http.get<IEnums>(this.getEnumJSON).pipe(
      tap((data) => console.log(JSON.stringify(data))),
      catchError(this.errorHandler)
    );
  }

  getEnumsSynchronous() {
    var response = new SyncRequestClient().get<IEnums>(this.getEnumJSON);
    return response;
  }

  getStatsdataScientist(filters: IDataScientistFilter) {
    let toSend = {
      total_amount_min: parseFloat(filters.total_amount_min.toString()),
      total_amount_max: parseFloat(filters.total_amount_max.toString()),

      trip_distance_min: parseFloat(filters.trip_distance_min.toString()),
      trip_distance_max: parseFloat(filters.trip_distance_max.toString()),

      extra_min: parseFloat(filters.extra_min.toString()),
      extra_max: parseFloat(filters.extra_max.toString()),

      fare_amount_min: filters.fare_amount_min,
      fare_amount_max: filters.fare_amount_max,

      improvement_surcharge_min: parseFloat(
        filters.improvement_surcharge_max.toString()
      ),
      improvement_surcharge_max: parseFloat(
        filters.improvement_surcharge_max.toString()
      ),
      mta_tax_min: parseFloat(filters.mta_tax_min.toString()),
      mta_tax_max: parseFloat(filters.mta_tax_max.toString()),
      passenger_count_min: parseFloat(filters.passenger_count_min.toString()),
      passenger_count_max: parseFloat(filters.passenger_count_max.toString()),
      tip_amount_min: parseFloat(filters.tip_amount_min.toString()),
      tip_amount_max: parseFloat(filters.tip_amount_max.toString()),
      tolls_amount_min: parseFloat(filters.tolls_amount_min.toString()),
      tolls_amount_max: parseFloat(filters.tolls_amount_max.toString()),
      ratecodeid: filters.ratecodeid,
      payment_type: filters.payment_type,
      vendorid: filters.vendorid,
      zone_depart: filters.zone_depart,
      zone_arrivee: filters.zone_arrivee,
    };
    return this.http
      .post<IDataScientistStats>(this.postFilterLink, toSend)
      .pipe(
        tap((data) => console.log('REPONSE du BACK ' + JSON.stringify(data))),
        catchError(this.errorHandler)
      );
  }

  errorHandler(error: HttpErrorResponse) {
    return observableThrowError(error.message || 'Server Error');
  }
}
