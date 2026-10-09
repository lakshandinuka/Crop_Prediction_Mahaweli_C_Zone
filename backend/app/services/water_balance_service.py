from __future__ import annotations


class WaterBalanceService:
    @staticmethod
    def estimate_water(
        crop: str,
        stage: str,
        etc_mm_day: float,
        effective_rainfall_mm_day: float,
        field_area_m2: float,
        irrigation_efficiency: float,
    ) -> dict:
        net_irrigation_mm_day = max(0.0, etc_mm_day - effective_rainfall_mm_day)
        gross_irrigation_depth_mm = net_irrigation_mm_day / (irrigation_efficiency / 100)
        net_volume_litres = net_irrigation_mm_day * field_area_m2
        gross_volume_litres = gross_irrigation_depth_mm * field_area_m2
        return {
            'crop': crop,
            'stage': stage,
            'etc_mm_day': etc_mm_day,
            'net_irrigation_mm_day': net_irrigation_mm_day,
            'gross_irrigation_depth_mm': gross_irrigation_depth_mm,
            'net_volume_litres': round(net_volume_litres, 2),
            'gross_volume_litres': round(gross_volume_litres, 2),
            'irrigation_efficiency_pct': irrigation_efficiency,
            'assumptions': 'Simplified daily screening estimate only; does not model root-zone storage, runoff, drainage, or crop-specific scheduling needs.',
        }
