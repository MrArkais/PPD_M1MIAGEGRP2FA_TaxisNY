import {
  throwError as observableThrowError,
  Observable,
  BehaviorSubject,
  Subject,
} from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { IVoyageurStats, IVoyageurFilter, IEnums } from '../interfaces';
import { tap, catchError } from 'rxjs/operators';
import { SyncRequestClient } from 'ts-sync-request/dist';

@Injectable()
export class VoyageurService {
  //private getStats = "http://localhost:8070/stats";
  //private getStatsJSON = "../../assets/stat.json"
  private postFilterLink = 'http://localhost:8070/voyageur';

  private getEnumJSON = '../../assets/enum.json';

  constructor(private http: HttpClient) {}

  statsfromVoyageur: any;

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

  getStatsVoyageurs(filters: IVoyageurFilter) {
    let toSend = {
      total_amount_min: parseFloat(filters.total_amount_min.toString()),
      total_amount_max: parseFloat(filters.total_amount_max.toString()),
      trip_distance_min: parseFloat(filters.trip_distance_min.toString()),
      trip_distance_max: parseFloat(filters.trip_distance_max.toString()),
      vendorid: filters.vendorid,
      zone_depart: filters.zone_depart,
      zone_arrivee: filters.zone_arrivee,
    };
    return this.http.post<IVoyageurStats>(this.postFilterLink, toSend).pipe(
      tap((data) => console.log('REPONSE du BACK ' + JSON.stringify(data))),
      catchError(this.errorHandler)
    );
  }

  errorHandler(error: HttpErrorResponse) {
    return observableThrowError(error.message || 'Server Error');
  }
}
