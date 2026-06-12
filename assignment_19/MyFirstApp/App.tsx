/**
 * Counter App with Theme Toggle
 * A simple React Native counter application with Light/Dark mode support.
 *
 * @format
 */

import React, {useState} from 'react';
import {
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

/* ──────────────────────────── Theme Definitions ──────────────────────────── */

const LIGHT_THEME = {
  background: '#FFFFFF',
  text: '#1A1A2E',
  buttonBg: '#4A90D9',
  buttonText: '#FFFFFF',
  resetBg: '#E74C3C',
  resetText: '#FFFFFF',
  toggleBg: '#6C5CE7',
  toggleText: '#FFFFFF',
  counterColor: '#2C3E50',
  subtitle: '#7F8C8D',
  statusBar: 'dark-content' as const,
};

const DARK_THEME = {
  background: '#1A1A2E',
  text: '#ECEFF4',
  buttonBg: '#4A90D9',
  buttonText: '#FFFFFF',
  resetBg: '#E74C3C',
  resetText: '#FFFFFF',
  toggleBg: '#A29BFE',
  toggleText: '#1A1A2E',
  counterColor: '#ECEFF4',
  subtitle: '#8899A6',
  statusBar: 'light-content' as const,
};

/* ──────────────────────────── Action Button ──────────────────────────────── */

interface ActionButtonProps {
  label: string;
  onPress: () => void;
  backgroundColor: string;
  textColor: string;
  flex?: number;
}

function ActionButton({
  label,
  onPress,
  backgroundColor,
  textColor,
  flex,
}: ActionButtonProps): React.JSX.Element {
  return (
    <TouchableOpacity
      style={[styles.button, {backgroundColor}, flex ? {flex} : null]}
      onPress={onPress}
      activeOpacity={0.7}>
      <Text style={[styles.buttonText, {color: textColor}]}>{label}</Text>
    </TouchableOpacity>
  );
}

/* ──────────────────────────── Main App ────────────────────────────────────── */

function App(): React.JSX.Element {
  const [count, setCount] = useState<number>(0);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  const theme = isDarkMode ? DARK_THEME : LIGHT_THEME;

  /* ── Counter handlers ── */

  const handleIncrement = (): void => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = (): void => {
    setCount(prevCount => (prevCount > 0 ? prevCount - 1 : 0));
  };

  const handleReset = (): void => {
    setCount(0);
  };

  /* ── Theme handler ── */

  const toggleTheme = (): void => {
    setIsDarkMode(prevMode => !prevMode);
  };

  return (
    <View style={[styles.container, {backgroundColor: theme.background}]}>
      <StatusBar barStyle={theme.statusBar} />

      {/* ── Title ── */}
      <Text style={[styles.title, {color: theme.text}]}>Counter App</Text>
      <Text style={[styles.subtitle, {color: theme.subtitle}]}>
        {isDarkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
      </Text>

      {/* ── Counter Display ── */}
      <View style={styles.counterContainer}>
        <Text style={[styles.counterValue, {color: theme.counterColor}]}>
          {count}
        </Text>
      </View>

      {/* ── Increment / Decrement Buttons (side-by-side) ── */}
      <View style={styles.rowButtons}>
        <ActionButton
          label="− Decrement"
          onPress={handleDecrement}
          backgroundColor={theme.buttonBg}
          textColor={theme.buttonText}
          flex={1}
        />
        <ActionButton
          label="+ Increment"
          onPress={handleIncrement}
          backgroundColor={theme.buttonBg}
          textColor={theme.buttonText}
          flex={1}
        />
      </View>

      {/* ── Reset Button ── */}
      <ActionButton
        label="↺ Reset"
        onPress={handleReset}
        backgroundColor={theme.resetBg}
        textColor={theme.resetText}
      />

      {/* ── Theme Toggle Button ── */}
      <View style={styles.toggleWrapper}>
        <ActionButton
          label={isDarkMode ? '☀️ Switch to Light Mode' : '🌙 Switch to Dark Mode'}
          onPress={toggleTheme}
          backgroundColor={theme.toggleBg}
          textColor={theme.toggleText}
        />
      </View>
    </View>
  );
}

/* ──────────────────────────── Styles ──────────────────────────────────────── */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 32,
  },
  counterContainer: {
    marginBottom: 40,
  },
  counterValue: {
    fontSize: 96,
    fontWeight: '800',
    textAlign: 'center',
  },
  rowButtons: {
    flexDirection: 'row',
    gap: 12,
    width: '100%',
    marginBottom: 12,
  },
  button: {
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    marginBottom: 0,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
  },
  toggleWrapper: {
    marginTop: 32,
    width: '100%',
  },
});

export default App;
