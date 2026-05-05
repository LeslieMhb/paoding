package com.qunar.paoding.controller;

import com.qunar.paoding.model.dto.*;
import com.qunar.paoding.service.TransportService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

/**
 * 交通查询接口
 */
@RestController
@RequestMapping("/api/v1/transport")
@RequiredArgsConstructor
public class TransportController {

    private final TransportService transportService;

    /** 搜索机票 */
    @PostMapping("/flight/search")
    public JsonV2<TransportListResult> searchFlights(@RequestBody FlightQueryRequest request) {
        return JsonV2.success(transportService.searchFlights(request));
    }

    /** 搜索火车票 */
    @PostMapping("/train/search")
    public JsonV2<TransportListResult> searchTrains(@RequestBody TrainQueryRequest request) {
        return JsonV2.success(transportService.searchTrains(request));
    }

    /** 综合搜索(机票+火车票) */
    @PostMapping("/search")
    public JsonV2<TransportListResult> searchTransport(
            @RequestBody FlightQueryRequest request) {
        TrainQueryRequest trainReq = TrainQueryRequest.builder()
                .depCity(request.getDepCity())
                .arrCity(request.getArrCity())
                .goDate(request.getGoDate())
                .adult(request.getAdult())
                .child(request.getChild())
                .build();
        return JsonV2.success(transportService.searchTransport(request, trainReq));
    }
}
