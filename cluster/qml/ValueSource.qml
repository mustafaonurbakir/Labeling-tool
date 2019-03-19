import QtQuick 2.2

Item {
    id: valueSource
	
	Connections {
        target: cluster
 
        onKphResult: {            
			valueSource.kph_old = valueSource.kph_new;
			valueSource.kph_new = kph;
			animation_id_1.running = true;
        }
 
        onPowerResult: {		
			valueSource.power_old = valueSource.power_new;
			valueSource.power_new = power;
        }
    }
    
	
    Timer {
        id: texttimer
        interval: 1000
        repeat: true
        running: true
        triggeredOnStart: true
        onTriggered: cluster.power() & cluster.kph()
    }
	

    //clusterın farklı hız aralıkları için
    property int imagine_kph: {
        if(kph<60){
            return kph*1.625
        }
        else{
            return 97.5+(kph-60)*0.8125
        }

    }
	property real kph_old: 0
    property real kph: 0
	property real kph_new: 0
	property real power_old: 0
    property real power: 0
	property real power_new: 0

    
    SequentialAnimation {
		id: animation_id_1
        running: false
        loops: 1
		

		ParallelAnimation {
			NumberAnimation {
				target: valueSource
				property: "kph"
				easing.type: Easing.InOutSine
				from: kph_old
				to: kph_new
				duration: 1000
			}
			NumberAnimation {
				target: valueSource
				property: "power"
				easing.type: Easing.InOutSine
				from: power_old
				to: power_new
				duration: 1000
			}
		}
    }
}
