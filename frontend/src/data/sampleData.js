// Sample device data
export const sampleDeviceData = [
    { id: 3, type: "Light", state: { power: "on", brightness: 95, color: "red", mode: "normal" }},
    { id: 4, type: "Speaker", state: { power: "off", volume: 50, mode: "normal" }},
    { id: 5, type: "Light", state: { power: "off", brightness: 100, color: "red", mode: "party" }},
    { id: 6, type: "Speaker", state: { power: "off", volume: 50, mode: "normal" }}
  ];
  
  // Sample usage data
  export const sampleUsageData = [
    { time: '00:00', lights: 4, speakers: 2 },
    { time: '04:00', lights: 1, speakers: 0 },
    { time: '08:00', lights: 2, speakers: 3 },
    { time: '12:00', lights: 3, speakers: 4 },
    { time: '16:00', lights: 5, speakers: 2 },
    { time: '20:00', lights: 6, speakers: 3 },
  ];