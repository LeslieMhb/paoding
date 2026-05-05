package com.qunar.paoding.controller;

import com.qunar.paoding.model.dto.AttractionListResult;
import com.qunar.paoding.model.dto.AttractionQueryRequest;
import com.qunar.paoding.model.dto.JsonV2;
import com.qunar.paoding.model.dto.RoutePlanResult;
import com.qunar.paoding.service.AttractionService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

/**
 * 景点查询接口
 */
@RestController
@RequestMapping("/api/v1/attraction")
@RequiredArgsConstructor
public class AttractionController {

    private final AttractionService attractionService;

    /** 搜索景点 */
    @PostMapping("/search")
    public JsonV2<AttractionListResult> searchAttractions(@RequestBody AttractionQueryRequest request) {
        return JsonV2.success(attractionService.searchAttractions(request));
    }

    /** 路线规划 */
    @PostMapping("/route/plan")
    public JsonV2<RoutePlanResult> planRoute(@RequestBody AttractionQueryRequest request) {
        return JsonV2.success(attractionService.planRoute(request));
    }
}
