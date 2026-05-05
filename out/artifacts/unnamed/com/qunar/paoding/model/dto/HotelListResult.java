package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 酒店搜索结果
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HotelListResult {

    /** 酒店列表 */
    @JsonProperty("hotelList")
    private List<HotelInfo> hotelList;

    /** 推荐标题 */
    @JsonProperty("recommendTitle")
    private String recommendTitle;

    /** 推荐副标题 */
    @JsonProperty("recommendSubTitle")
    private String recommendSubTitle;

    /** 更多酒店链接 */
    @JsonProperty("recommendMoreScheme")
    private String recommendMoreScheme;
}
