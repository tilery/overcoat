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
  [zoom>=7][sov = null] {
  	text-size: 16;
  }
  [sov != null] {
    text-name: [name] + ' ('+[sov]+')';
    text-size: 12;
  }
}

#boundary_label_low[zoom>=6][zoom<=10] {
  text-name: [name];
  text-size: 11;
  text-face-name: @regular;
  text-placement: point;
  text-fill: @state_text;
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-wrap-width: 50;
  text-label-position-tolerance: 100;
  text-margin: 7;
  [zoom>=7] {
    text-size: 13;
    text-wrap-width: 65;
    text-halo-radius: 2;
    text-line-spacing: 1;
  }
  [zoom>=9] {
    text-face-name: @bold;
    text-size: 18;
    text-character-spacing: 2;
    text-wrap-width: 100;
    text-line-spacing: 2;
    text-label-position-tolerance: 200;
  }
}
#city[zoom>=5][zoom<=10],
#place_low[type='city'][zoom>=7][zoom<=10],
#place_low[type='town'][zoom>=9][zoom<=10] {
  shield-file: url('icon/place/[type].svg');
  shield-name:[name];
  shield-size: 11;
  shield-face-name: @regular;
  shield-halo-radius: 1;
  shield-wrap-width: 50;
  shield-fill: @town_text;
  shield-halo-fill: @halo;
  shield-placement-type: simple;
  shield-placements: 'NE,SW,NW,SE,E,W,N,S';
  shield-text-dy: 2;
  shield-text-dx: 6;
  shield-unlock-image: true;
  shield-min-distance: 10;
  [type='town'] {
    shield-text-dx: 4;
    shield-text-dy: 4;
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
    shield-size: 12;
    shield-allow-overlap: true;
  }
  [type='intermediate'] {
    shield-face-name: @medium;
    shield-fill: @city_text;
    shield-size: 11;
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
      shield-size: 17;
      shield-placements: 'N';
      shield-text-dy: 8;
    }
    [type='city'] {
      shield-size: 14;
    }
  }
}
#city[zoom>10],
#place[type='city'][zoom>10],
#place[type='town'][zoom>10],
#place[type='village'][zoom>=11],
#place[type='minor'][zoom>=14] {
  text-name: '[name]';
  [lang='fr'] {
    text-name: '[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  }
  text-face-name: @light;
  text-placement: point;
  text-fill: @village_text;
  text-size: 11;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 45;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-line-spacing: -2;
  text-margin: 30;
  text-min-padding: 1;
  [type='town'] {
    text-fill: @town_text;
    text-face-name: @regular;
    text-size: 13;
  }
  [type='city'] {
    text-fill: @city_text;
    text-face-name: @medium;
    text-size: 14;
  }
  [type='intermediate'], [type='embassy'], [type='capital'] {
    text-face-name: @bold;
  	text-size:16;
  }
  [type='minor'] {
    text-margin: 50;
  }
  [zoom>=12] {
    text-margin: 10;
    text-min-padding: 1;
    text-size: 12;
    [type='town'] {
      text-size: 14;
    }
    [type='city'] {
      text-size: 16;
    }
    [type='intermediate'], [type='embassy'], [type='capital'] {
      text-size: 18;
    }
  }
  [zoom>=13] {
    text-size: 13;
    [type='minor'] {
      text-size: 10;
    }
    [type='town'] {
      text-size: 15;
    }
    [type='city'] {
      text-size: 17;
    }
    [type='intermediate'], [type='embassy'], [type='capital'] {
      text-size: 19;
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
