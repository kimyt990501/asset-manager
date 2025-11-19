import { defineStore } from 'pinia'
import { summaryAPI } from '@/services/api'

interface SummaryState {
    totalAssets: number
    monthlyFixedIncome: number
    monthlyFixedExpenses: number
    netMonthlyCashflow: number
    netWorthTrend: {
        labels: string[]
        data: number[]
    }
    loading: boolean
    error: string | null
}

export const useSummaryStore = defineStore('summary', {
    state: (): SummaryState => ({
        totalAssets: 0,
        monthlyFixedIncome: 0,
        monthlyFixedExpenses: 0,
        netMonthlyCashflow: 0,
        netWorthTrend: {
            labels: [],
            data: []
        },
        loading: false,
        error: null
    }),

    actions: {
        async fetchSummary() {
            this.loading = true
            this.error = null
            try {
                const response = await summaryAPI.getFullSummary()
                const data = response.data
                this.totalAssets = data.total_assets
                this.monthlyFixedIncome = data.monthly_income
                this.monthlyFixedExpenses = data.monthly_fixed_expenses
                this.netMonthlyCashflow = data.net_monthly_cashflow
            } catch (err) {
                console.error('Failed to fetch summary:', err)
                this.error = '요약 정보를 불러오는데 실패했습니다.'
            } finally {
                this.loading = false
            }
        },

        async fetchTrend(months: number = 6) {
            try {
                const response = await summaryAPI.getNetWorthTrend(months)
                this.netWorthTrend = response.data
            } catch (err) {
                console.error('Failed to fetch trend:', err)
                // Keep previous data or set empty on error?
                // For now, just log error.
            }
        }
    }
})
