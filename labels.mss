#country[prio<=3][zoom=3],
#country[prio<=4][zoom=4],
#country[zoom>=5][zoom<=10] {
  text-name: [name];
  text-size: 11;
  text-face-name: @bold;
  text-placement: point;
  text-fill: @country_text;
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-wrap-width: 40;
  text-label-position-tolerance: 20;
  text-character-spacing: 1;
  text-placement-type: simple;
  text-placements: 'N,S';
  text-line-spacing: 0.1;
  text-margin: 7;
  [zoom>=5][sov = null] {
    text-size: 14;
    text-margin: 5;
    text-dx: 10;
    text-dy: 10;
    text-wrap-width: 60;
  }
  [sov != null] {
    text-name: [name] + ' ('+[sov]+')';
    text-size: 12;
  }
}

#boundary_label_low[zoom>=7][zoom<=10] {
  text-name: '[name]';
  text-face-name: @medium;
  text-placement: point;
  text-fill: @state_text;
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-size: 10;
  text-wrap-width: 40;
  text-margin: 30;
  [zoom>=7] {
    text-size: 11;
    text-wrap-width: 50;
  }
  [zoom>=8] {
    text-halo-radius: 2;
    text-line-spacing: 1;
  }
  [zoom>=9] {
    text-size: 12;
    text-character-spacing: 1;
    text-wrap-width: 80;
    text-line-spacing: 2;
  }
  [zoom>=10] {
    text-size: 14;
    text-character-spacing: 2;
  }
}
#city[zoom>=5][zoom<=10],
#place_low[type='city'][zoom>=7][zoom<=10],
#place_low[type='town'][zoom>=9][zoom<=10] {
  shield-file: url('icon/place/[type].svg');
  shield-name:'[name]';
  shield-size: 11;
  shield-face-name: @regular;
  shield-halo-radius: 1;
  shield-wrap-width: 50;
  shield-fill: @town_text;
  shield-halo-fill: @halo;
  shield-placement-type: simple;
  shield-placements: 'NE,SW,NW,SE,E,W';
  shield-text-dy: 2;
  shield-text-dx: 6;
  shield-unlock-image: true;
  shield-min-distance: 10;
  [type='town'] {
    shield-text-dx: 2;
  }
  [type='city'] {
    shield-line-spacing: -2;
    shield-face-name: @medium;
    shield-fill: @city_text;
    shield-text-dy: 4;
  }
  [type='embassy'], [type='capital'] {
    shield-fill: @city_text;
    shield-face-name: @bold;
    shield-size: 13;
    [type='embassy'] {
      shield-allow-overlap: true;
    }
  }
  [type='intermediate'] {
    shield-face-name: @medium;
    shield-fill: @city_text;
    shield-size: 12;
  }
  [ldir!=null] {
    shield-placements: '[ldir]';
    [ldir='N'],[ldir='S'] {
      shield-text-dy: 8;
    }
  }
  [zoom>=9] {
    shield-size: 12;
    [type='embassy'], [type='capital'], [type='intermediate'] {
      shield-size: 15;
    }
  }
}
#place[type='city'][zoom>=10],
#place[type='town'][zoom>=10],
#place[type='village'][zoom>=9],
#place[type='minor'][zoom>=14] {
  text-name: '[name]';
  [lang='fr'] {
    text-name: '[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  }
  text-face-name: @light;
  text-placement: point;
  text-fill: @village_text;
  text-size: 12;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 40;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-line-spacing: -2;
  text-margin: 30;
  text-min-padding: 1;
  [type='town'] {
    text-fill: @town_text;
    text-face-name: @regular;
  }
  [type='city'] {
    text-fill: @city_text;
    text-face-name: @medium;
  }
  [type='minor'] {
    text-margin: 50;
  }
  [zoom>=12] {
    text-margin: 10;
    text-min-padding: 1;
    text-size: 13;
    [type='city'] {
      text-size: 14;
    }
  }
  [zoom>=13] {
    text-size: 14;
    [type='city'] {
      text-size: 15;
    }
  }
  [zoom>=14] {
    text-size: 15;
    [type='minor'] {
      text-size: 10;
    }
  }
}


#waterway_label_low[zoom>=12][zoom<17],
#waterway_label[zoom>=17] {
  text-name: '[name]';
  text-face-name: @regular;
  text-fill: darken(@water, 25);
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-placement: line;
  text-min-distance: 300;
  text-size: 12;
  text-label-position-tolerance: 50;
  [zoom>=15] {
    text-size: 13;
  }
}
