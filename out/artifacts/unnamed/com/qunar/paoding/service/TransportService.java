package com.qunar.paoding.service;

import com.qunar.paoding.model.dto.*;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

/**
 * 交通服务 - Mock实现
 */
@Service
public class TransportService {

    public TransportListResult searchFlights(FlightQueryRequest request) {
        List<FlightInfo> flights = buildMockFlights(request.getDepCity(), request.getArrCity(), request.getGoDate());
        return TransportListResult.builder()
                .flightList(flights)
                .trainList(List.of())
                .recommendTitle("共找到" + flights.size() + "个航班")
                .recommendSubTitle(request.getDepCity() + "→" + request.getArrCity() + " 精选航班")
                .recommendMoreFlightScheme("qunar://flight/list?dep=" + request.getDepCity() + "&arr=" + request.getArrCity())
                .build();
    }

    public TransportListResult searchTrains(TrainQueryRequest request) {
        List<TrainInfo> trains = buildMockTrains(request.getDepCity(), request.getArrCity(), request.getGoDate());
        return TransportListResult.builder()
                .flightList(List.of())
                .trainList(trains)
                .recommendTitle("共找到" + trains.size() + "个车次")
                .recommendSubTitle(request.getDepCity() + "→" + request.getArrCity() + " 精选车次")
                .recommendMoreTrainScheme("qunar://train/list?dep=" + request.getDepCity() + "&arr=" + request.getArrCity())
                .build();
    }

    public TransportListResult searchTransport(FlightQueryRequest flightReq, TrainQueryRequest trainReq) {
        List<FlightInfo> flights = buildMockFlights(flightReq.getDepCity(), flightReq.getArrCity(), flightReq.getGoDate());
        List<TrainInfo> trains = buildMockTrains(trainReq.getDepCity(), trainReq.getArrCity(), trainReq.getGoDate());
        return TransportListResult.builder()
                .flightList(flights)
                .trainList(trains)
                .recommendTitle("共找到" + (flights.size() + trains.size()) + "个结果，为您推荐")
                .recommendSubTitle(flightReq.getDepCity() + "→" + flightReq.getArrCity() + " 精选路线")
                .recommendMoreFlightScheme("qunar://flight/list?dep=" + flightReq.getDepCity() + "&arr=" + flightReq.getArrCity())
                .recommendMoreTrainScheme("qunar://train/list?dep=" + trainReq.getDepCity() + "&arr=" + trainReq.getArrCity())
                .build();
    }

    private List<FlightInfo> buildMockFlights(String depCity, String arrCity, String goDate) {
        return Arrays.asList(
                FlightInfo.builder()
                        .transfer(false)
                        .transportNo("CA1501")
                        .departureTime("07:30")
                        .arrivalTime("09:45")
                        .timeInterval("2h15m")
                        .departureStation(depCity + "萧山国际机场")
                        .arrivalStation(arrCity + "首都国际机场T3")
                        .departure(depCity)
                        .arrival(arrCity)
                        .totalPrice(56000)
                        .freeLuggage("20kg")
                        .carrier("中国国航")
                        .goDate(goDate)
                        .build(),
                FlightInfo.builder()
                        .transfer(false)
                        .transportNo("MU5101")
                        .departureTime("10:00")
                        .arrivalTime("12:20")
                        .timeInterval("2h20m")
                        .departureStation(depCity + "萧山国际机场")
                        .arrivalStation(arrCity + "首都国际机场T2")
                        .departure(depCity)
                        .arrival(arrCity)
                        .totalPrice(48000)
                        .freeLuggage("23kg")
                        .carrier("东方航空")
                        .goDate(goDate)
                        .build(),
                FlightInfo.builder()
                        .transfer(false)
                        .transportNo("CZ6151")
                        .departureTime("14:30")
                        .arrivalTime("16:50")
                        .timeInterval("2h20m")
                        .departureStation(depCity + "萧山国际机场")
                        .arrivalStation(arrCity + "大兴国际机场")
                        .departure(depCity)
                        .arrival(arrCity)
                        .totalPrice(42000)
                        .freeLuggage("20kg")
                        .carrier("南方航空")
                        .goDate(goDate)
                        .build(),
                FlightInfo.builder()
                        .transfer(true)
                        .transportNo("HU7607")
                        .departureTime("08:00")
                        .arrivalTime("12:30")
                        .timeInterval("4h30m")
                        .departureStation(depCity + "萧山国际机场")
                        .arrivalStation(arrCity + "首都国际机场T1")
                        .departure(depCity)
                        .arrival(arrCity)
                        .transSpot("南京")
                        .crossDaysDesc("")
                        .totalPrice(35000)
                        .freeLuggage("20kg")
                        .carrier("海南航空")
                        .goDate(goDate)
                        .build()
        );
    }

    private List<TrainInfo> buildMockTrains(String depCity, String arrCity, String goDate) {
        return Arrays.asList(
                TrainInfo.builder()
                        .isTransfer(false)
                        .transportNo("G34")
                        .departureTime("07:15")
                        .arrivalTime("12:38")
                        .timeInterval("5h23m")
                        .departureStation(depCity + "东站")
                        .arrivalStation(arrCity + "南站")
                        .departure(depCity)
                        .arrival(arrCity)
                        .seatType("二等座")
                        .totalPrice(63100)
                        .goDate(goDate)
                        .trainType("高铁")
                        .build(),
                TrainInfo.builder()
                        .isTransfer(false)
                        .transportNo("G40")
                        .departureTime("09:15")
                        .arrivalTime("14:28")
                        .timeInterval("5h13m")
                        .departureStation(depCity + "东站")
                        .arrivalStation(arrCity + "南站")
                        .departure(depCity)
                        .arrival(arrCity)
                        .seatType("一等座")
                        .totalPrice(104900)
                        .goDate(goDate)
                        .trainType("高铁")
                        .build(),
                TrainInfo.builder()
                        .isTransfer(false)
                        .transportNo("D710")
                        .departureTime("21:30")
                        .arrivalTime("07:30+1")
                        .timeInterval("10h0m")
                        .departureStation(depCity + "站")
                        .arrivalStation(arrCity + "站")
                        .departure(depCity)
                        .arrival(arrCity)
                        .seatType("动卧")
                        .totalPrice(53000)
                        .goDate(goDate)
                        .trainType("动车")
                        .build(),
                TrainInfo.builder()
                        .isTransfer(false)
                        .transportNo("T32")
                        .departureTime("18:20")
                        .arrivalTime("09:52+1")
                        .timeInterval("15h32m")
                        .departureStation(depCity + "站")
                        .arrivalStation(arrCity + "站")
                        .departure(depCity)
                        .arrival(arrCity)
                        .seatType("硬卧")
                        .totalPrice(26300)
                        .goDate(goDate)
                        .trainType("普快")
                        .build()
        );
    }
}
