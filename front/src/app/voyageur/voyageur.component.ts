import { Component, OnInit, Input, Output } from '@angular/core';
import { FormControl } from '@angular/forms';

import { VoyageurService } from '../services/voyageur.service';
import { IVoyageurStats, IVoyageurFilter, IEnums } from '../interfaces';
import { Options } from 'ng5-slider';

@Component({
  selector: 'app-voyageur',
  templateUrl: './voyageur.component.html',
  styleUrls: ['./voyageur.component.scss'],
})
export class VoyageurComponent implements OnInit {
  @Input()
  title: string;
  stats: any;
  enums: any;
  mode: string;

  filter: IVoyageurFilter;
  thumbLabel = true;
  selectedAmount = 2;
  selectedDistance = 3;
  selectedZoneDep = [];
  selectedZoneArr = [];
  selectedVendorId = [];

  panelOpenState = false;
  zoneDEP = new FormControl();
  zoneARR = new FormControl();
  vendorID = new FormControl();

  optionsPrix: Options = {
    floor: 1,
    ceil: 200,
  };
  valuePrix: number = this.optionsPrix.floor;
  highValuePrix: number = this.optionsPrix.ceil;

  optionsDist: Options = {
    floor: 1,
    ceil: 300,
  };
  valueDist: number = this.optionsDist.floor;
  highValueDist: number = this.optionsDist.ceil;

  showSpinner = false;

  constructor(private voyageurService: VoyageurService) {}

  ngOnInit() {
    this.title = 'Voyageur';
    this.mode='voyageur';
    // this.voyageurService.getEnums()
    //   .switchMap(enums => {
    //     this.InitVoyageur(enums.zones);
    //   })
    //   .subscribe((voyageur: IVoyageur[]) => (this.voyageur = voyageur));
    this.enums = this.voyageurService.getEnumsSynchronous();
    this.InitVoyageur(this.enums);
  }

  InitVoyageur(enn: IEnums) {
    this.showSpinner = true;
    this.zoneDEP.setValue(enn.zones);
    this.zoneARR.setValue(enn.zones);
    this.vendorID.setValue(['1', '2']);
    let basicFilter = {
      total_amount_min: this.optionsPrix.floor,
      total_amount_max: this.optionsPrix.ceil,
      trip_distance_min: this.optionsDist.floor,
      trip_distance_max: this.optionsDist.ceil,
      vendorid: this.vendorID.value,
      zone_depart: this.zoneDEP.value,
      zone_arrivee: this.zoneARR.value,
    } as IVoyageurFilter;

    // AVEC COMMENTAIRE

    this.voyageurService
      .getStatsVoyageurs(basicFilter)
      .subscribe((data: IVoyageurStats) => {
        this.stats = data;
        this.showSpinner = false;
      });

    console.log('FILTRES BASIC A ENVOYER :', basicFilter);

    // this.voyageurService
    // .getStatsVoyageurJSON().subscribe((data: IVoyageurStats[]) =>
    // this.stats = data
    // )
  }

  selectAll_zonesDepart(ev) {
    if (ev._selected) {
      this.zoneDEP.setValue(this.enums.zones);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.zoneDEP.setValue([]);
    }

  }

  selectAll_zonesArrivee(ev) {
    if (ev._selected) {
      this.zoneARR.setValue(this.enums.zones);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.zoneARR.setValue([]);
    }

  }
  selectAll_vendorId(ev) {
    let ven = [];

    if (ev._selected) {
      for (let v of this.enums.vendors) {
        ven.push(v['id'].toString());
      }
      this.vendorID.setValue(ven);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.vendorID.setValue([]);
    }
  
  }

  postFilter() {
    console.log('Post request function');
    this.showSpinner = true;

    let filters = {
      total_amount_min: parseFloat(this.valuePrix.toString()),
      total_amount_max: parseFloat(this.highValuePrix.toString()),
      trip_distance_min: parseFloat(this.valueDist.toString()),
      trip_distance_max: parseFloat(this.highValueDist.toString()),
      vendorid: this.vendorID.value,
      zone_depart: this.zoneDEP.value,
      zone_arrivee: this.zoneARR.value,
    } as IVoyageurFilter;

    console.log('FILTRES A ENVOYER :', filters);

    // let basicFilter = {
    //   total_amount_min: 5,
    //   total_amount_max: 200,
    //   trip_distance_min: 10,
    //   trip_distance_max: 100,
    //   vendorid: ['1'],
    //   zone_depart: enn.zones,
    //   zone_arrivee: enn.zones,
    // } as IVoyageurFilter;

    this.voyageurService.getStatsVoyageurs(filters).subscribe((data: any) => {
      this.stats = data;
      this.showSpinner = false;
    });
  }
}
