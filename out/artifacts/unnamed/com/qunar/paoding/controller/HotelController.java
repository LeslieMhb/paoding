package com.qunar.paoding.controller;

import com.qunar.paoding.model.dto.HotelInfo;
import com.qunar.paoding.model.dto.HotelListResult;
import com.qunar.paoding.model.dto.HotelQueryRequest;
import com.qunar.paoding.model.dto.JsonV2;
import com.qunar.paoding.service.HotelService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

/**
 * 酒店查询接口
 */
@RestController
@RequestMapping("/api/v1/hotel")
@RequiredArgsConstructor
public class HotelController {

    private final HotelService hotelService;

    /** 搜索酒店 */
    @PostMapping("/search")
    public JsonV2<HotelListResult> searchHotels(@RequestBody HotelQueryRequest request) {
        return JsonV2.success(hotelService.searchHotels(request));
    }

    /** 获取酒店详情 */
    @GetMapping("/detail/{hotelSeq}")
    public JsonV2<HotelInfo> getHotelDetail(@PathVariable String hotelSeq) {
        return JsonV2.success(hotelService.getHotelDetail(hotelSeq));
    }
}
