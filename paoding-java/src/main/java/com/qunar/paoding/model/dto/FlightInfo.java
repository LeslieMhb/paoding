package com.qunar.paoding.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 航班信息
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class FlightInfo {

    /** 是否中转 */
    @JsonProperty("transfer")
    @Builder.Default
    private Boolean transfer = false;

    /** 航班号 */
    @JsonProperty("transportNo")
    private String transportNo;

    /** 出发时间 */
    @JsonProperty("departureTime")
    private String departureTime;

    /** 到达时间 */
    @JsonProperty("arrivalTime")
    private String arrivalTime;

    /** 飞行时长描述 */
    @JsonProperty("timeInterval")
    private String timeInterval;

    /** 出发机场 */
    @JsonProperty("departureStation")
    private String departureStation;

    /** 到达机场 */
    @JsonProperty("arrivalStation")
    private String arrivalStation;

    /** 出发城市 */
    @JsonProperty("departure")
    private String departure;

    /** 到达城市 */
    @JsonProperty("arrival")
    private String arrival;

    /** 中转地 */
    @JsonProperty("transSpot")
    private String transSpot;

    /** 跨天描述 */
    @JsonProperty("crossDaysDesc")
    private String crossDaysDesc;

    /** 总价(分) */
    @JsonProperty("totalPrice")
    private Integer totalPrice;

    /** 免费行李额 */
    @JsonProperty("freeLuggage")
    private String freeLuggage;

    /** 承运航司 */
    @JsonProperty("carrier")
    private String carrier;

    /** 出发日期 */
    @JsonProperty("goDate")
    private String goDate;
}
