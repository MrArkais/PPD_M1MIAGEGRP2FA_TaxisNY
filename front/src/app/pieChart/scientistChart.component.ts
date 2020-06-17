import {
  Component,
  OnInit,
  OnChanges,
  Input,
  Output,
  EventEmitter,
  SimpleChanges,
} from '@angular/core';

import * as CanvasJS from './canvasjs.min.js';
import { IPieDatas, IPlotDatas } from '../interfaces';
import { DataScientistService } from '../services/datascientist.service';
import { IEnums } from '../interfaces';

@Component({
  selector: 'app-scientistChart',
  templateUrl: './scientistChart.component.html',
  styleUrls: ['./scientistChart.component.scss'],
})
export class ScientistChartComponent implements OnInit, OnChanges {
  @Input() statschild: any;
  enums: any;

  datasD: IPieDatas[] = [];
  datasA: IPieDatas[] = [];
  datasPayment: IPlotDatas[] = [];

  datasFare: IPieDatas[] = [];

  datasTips: IPieDatas[] = [];

  constructor(private dataScientistService: DataScientistService) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['statschild']) {
      this.buildChart();
    }
  }

  ngOnInit() {
    this.enums = this.dataScientistService.getEnums();
    this.buildChart();
  }

  buildChart() {
    this.datasD = [];
    this.datasA = [];
    this.datasPayment = [];
    this.datasFare = [];
    this.datasTips= []

    let zonesD = this.statschild.zone_depart_distinct;
    let zonesA = this.statschild.zone_arrivee_distinct;
    let paymentType = this.statschild.paiement_type_distinct;
    let fare = this.statschild.fare_amount_distinct;
    let tip = this.statschild.tip_amount_distinct;

    for (let z of zonesD) {
      let dep = { y: z.count, name: z.zone_depart } as IPieDatas;
      this.datasD.push(dep);
    }

    for (let z of zonesA) {
      let arr = { y: z.count, name: z.zone_arrivee } as IPieDatas;
      this.datasA.push(arr);
    }

    for (let z of paymentType) {
      let pay = {
        y: z.count,
        name: this.setPaymentNames(z.payment_type),
      } as IPieDatas;

      this.datasPayment.push(pay);
    }

    for (let z of fare) {
      let fare = { y: z.count, name: z.fare_amount } as IPieDatas;

      this.datasFare.push(fare);
    }


    for (let z of tip) {
      let tips = { y: z.count, name: z.tip_amount } as IPieDatas;

      this.datasTips.push(tips);
    }

    //   let chart = new CanvasJS.Chart('chartContainer', {
    //     theme: 'light2',
    //     animationEnabled: true,
    //     exportEnabled: true,
    //     title: {
    //       text: 'Répartition de zones de départ',
    //     },
    //     data: [
    //       {
    //         type: 'pie',
    //         showInLegend: true,
    //         toolTipContent: '<b>{name}</b>: {y} (#percent%)',
    //         indexLabel: '{name} - #percent%',
    //         dataPoints: this.datasD,
    //       },
    //     ],
    //   });

    

    let chart = new CanvasJS.Chart('chartContainer', {
      theme: 'light2',
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: 'Répartition par type de paiement',
      },

      data: [
        {
          type: 'column',
          showInLegend: true,
          toolTipContent: '<b>{name}</b>: {y}',
          indexLabel: '{name}',
          dataPoints: this.datasPayment,
        },
      ],
    });

  
    let chart2 = new CanvasJS.Chart('chartContainer2', {
      theme: 'light2',
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: 'Répartition du tarif',
      },
      subtitles: [
        {
          text:
            'Le tarif est calculé en fonction du temps et de la distance par le compteur du taxi. ',
        },
      ],
      axisX: {
        title: 'Tarif',
      },
      axisY: {
        title: 'Quantité',
      },

      data: [
        {
          type: 'column',
          showInLegend: true,
          toolTipContent: '<b>{name} $</b>: {y}',
          indexLabel: '{name}',
          dataPoints: this.datasFare,
        },
      ],
    });

    let chart3 = new CanvasJS.Chart('chartContainer3', {
      theme: 'light2',
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: 'Répartition des tips',
      },
      
      axisX: {
        title: 'Tips',
      },
      axisY: {
        title: 'Quantité',
      },

      data: [
        {
          type: 'column',
          showInLegend: true,
          toolTipContent: '<b>{name} $</b>: {y}',
          indexLabel: '{name}',
          dataPoints: this.datasTips,
        },
      ],
    });


    chart.render();
    chart2.render();
    chart3.render();
  }

  setPaymentNames(id): string {
    let name;
    let payment = {
      payment_type: [
        {
          id: 1,
          name: 'Carte de crédit',
        },
        {
          id: 2,
          name: 'Espèces',
        },
        {
          id: 3,
          name: 'Non pris en charge',
        },
        {
          id: 4,
          name: 'Litige',
        },
        {
          id: 5,
          name: 'Inconnu',
        },
        {
          id: 6,
          name: 'Course annulée',
        },
      ],
    };
    payment.payment_type.forEach((element) => {
      if (element.id == id) {
        name = element.name;
      }
    });

    return name;
  }
}
