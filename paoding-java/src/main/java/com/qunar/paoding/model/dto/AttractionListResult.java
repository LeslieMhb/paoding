package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 景点搜索结果
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AttractionListResult {

    /** 景点列表 */
    @JsonProperty("attractionList")
    private List<AttractionInfo> attractionList;

    /** 推荐标题 */
    @JsonProperty("recommendTitle")
    private String recommendTitle;

    /** 推荐副标题 */
    @JsonProperty("recommendSubTitle")
    private String recommendSubTitle;
}
