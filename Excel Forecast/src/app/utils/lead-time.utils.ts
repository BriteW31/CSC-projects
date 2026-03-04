export class LeadTimeUtils {
  
  static getMaxLeadTimeDays(leadTimes: number[]): number {
    return Math.max(...leadTimes);
  }

  static getAverageLeadTimeDays(leadTimes: number[]): number {
    const sum = leadTimes.reduce((a, b) => a + b, 0);
    // Mimicking Python's round(sum / 10). 
    // Note: Python's round() rounds to nearest even number for .5, JS rounds up.
    // Usually Math.round is sufficient for this context.
    return Math.round(sum / 10);
  }

  static getMaxLeadTimeMonths(leadTimes: number[]): number {
    const maxDays = this.getMaxLeadTimeDays(leadTimes);
    return maxDays / 30.5;
  }

  static getAverageLeadTimeMonths(leadTimes: number[]): number {
    const averageDays = this.getAverageLeadTimeDays(leadTimes);
    const months = averageDays / 30.5;
    // Round to 2 decimal places
    return Math.round(months * 100) / 100;
  }

  static getSDLeadTimesDays(leadTimes: number[]): number {
    if (leadTimes.length < 2) {
      return 0; // Standard deviation is not defined for 1 or 0 values
    }

    const average = this.getAverageLeadTimeDays(leadTimes);
    
    const sumSquaredDiff = leadTimes.reduce((acc, lead) => {
      return acc + Math.pow(lead - average, 2);
    }, 0);

    const variance = sumSquaredDiff / (leadTimes.length - 1); // Sample standard deviation
    return Math.sqrt(variance);
  }

  static getSDLeadTimesMonths(leadTimes: number[]): number {
    const sd = this.getSDLeadTimesDays(leadTimes);
    return sd / 30.5;
  }
}
