package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 火车票信息
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TrainInfo {

    /** 是否中转 */
    @JsonProperty("isTransfer")
    @Builder.Default
    private Boolean isTransfer = false;

    /** 车次号 */
    @JsonProperty("transportNo")
    private String transportNo;

    /** 出发时间 */
    @JsonProperty("departureTime")
    private String departureTime;

    /** 到达时间 */
    @JsonProperty("arrivalTime")
    private String arrivalTime;

    /** 行驶时长描述 */
    @JsonProperty("timeInterval")
    private String timeInterval;

    /** 出发站 */
    @JsonProperty("departureStation")
    private String departureStation;

    /** 到达站 */
    @JsonProperty("arrivalStation")
    private String arrivalStation;

    /** 出发城市 */
    @JsonProperty("departure")
    private String departure;

    /** 到达城市 */
    @JsonProperty("arrival")
    private String arrival;

    /** 座位类型 */
    @JsonProperty("seatType")
    private String seatType;

    /** 票价(分) */
    @JsonProperty("totalPrice")
    private Integer totalPrice;

    /** 出发日期 */
    @JsonProperty("goDate")
    private String goDate;

    /** 列车类型(高铁/动车/普快等) */
    @JsonProperty("trainType")
    private String trainType;
}
