export interface IVoyageurStats {
  zone_depart_distinct: any[],
  zone_arrivee_distinct : any[],
  moyenne : any[],
  metrique : any[]  
}

export interface IVoyageurFilter {
  total_amount_min: number,
  total_amount_max: number,
  trip_distance_min: number,
  trip_distance_max: number,
  vendorid: string[], 
  zone_depart: string[],
  zone_arrivee: string[]
}

export interface IDataScientistStats {

  moyenne : any[],
  metrique : any[],
  zone_depart_distinct: any[],
  zone_arrivee_distinct : any[], 
}


export interface IDataScientistFilter {
  total_amount_min: number,
  total_amount_max: number,
  trip_distance_min: number,
  trip_distance_max: number,
  extra_min: number,
  extra_max: number,
  fare_amount_min: number,
  fare_amount_max: number,
  improvement_surcharge_min: number,
  improvement_surcharge_max: number,
  mta_tax_min: number,
  mta_tax_max: number,
  passenger_count_min: number,
  passenger_count_max: number,
  tip_amount_min: number,
  tip_amount_max: number,
  tolls_amount_min: number,
  tolls_amount_max: number,
  ratecodeid: string[],
  payment_type: string[],
  vendorid: string[], 
  zone_depart: string[],
  zone_arrivee: string[]
}


export interface IEnums{
  zones : string[],
  vendors : any[],
  payment_type: any[],
  rate_code: []
}

export interface IPieDatas{
  y : number,
  name : string
}

export interface IPlotDatas{
  y : number,
  name : string
}


export interface LoaderState {
  show: boolean;
}
